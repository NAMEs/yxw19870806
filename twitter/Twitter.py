# -*- coding:UTF-8  -*-
'''
Created on 2014-5-31

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
如有问题或建议请联系
'''

from common import common, json
import os
import re
import threading
import time

IS_TRACE = False
IS_SHOW_ERROR = False
IS_SHOW_STEP = False
TRACE_LOG_PATH = ''
ERROR_LOG_PATH = ''
STEP_LOG_PATH = ''
THREAD_COUNT = 0

threadLock = threading.Lock()


def trace(msg):
    threadLock.acquire()
    common.trace(msg, IS_TRACE, TRACE_LOG_PATH)
    threadLock.release()


def print_error_msg(msg):
    threadLock.acquire()
    common.print_error_msg(msg, IS_SHOW_ERROR, ERROR_LOG_PATH)
    threadLock.release()


def print_step_msg(msg):
    threadLock.acquire()
    common.print_step_msg(msg, IS_SHOW_STEP, STEP_LOG_PATH)
    threadLock.release()

class Twitter(common.Robot):

    def __init__(self, user_id_list_file_path='', image_download_path='', image_temp_path=''):
        global INIT_MAX_ID
        global GET_IMAGE_COUNT
        global IMAGE_TEMP_PATH
        global IMAGE_DOWNLOAD_PATH
        global NEW_USER_ID_LIST_FILE_PATH
        global IS_SORT
        global IS_TRACE
        global IS_SHOW_ERROR
        global IS_SHOW_STEP
        global TRACE_LOG_PATH
        global ERROR_LOG_PATH
        global STEP_LOG_PATH

        # multiprocessing.Process.__init__(self)
        common.Robot.__init__(self)

        if user_id_list_file_path != '':
            self.user_id_list_file_path = user_id_list_file_path
        INIT_MAX_ID = 999999999999999999
        GET_IMAGE_COUNT = self.get_image_count
        if image_temp_path != '':
            IMAGE_TEMP_PATH = image_temp_path
        else:
            IMAGE_TEMP_PATH = self.image_temp_path
        if image_download_path != '':
            IMAGE_DOWNLOAD_PATH = image_download_path
        else:
            IMAGE_DOWNLOAD_PATH = self.image_download_path
        IS_SORT = self.is_sort
        IS_TRACE = self.is_trace
        IS_SHOW_ERROR = self.is_show_error
        IS_SHOW_STEP = self.is_show_step
        NEW_USER_ID_LIST_FILE_PATH = os.getcwd() + "\\info\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(self.user_id_list_file_path)[-1]
        TRACE_LOG_PATH = self.trace_log_path
        ERROR_LOG_PATH = self.error_log_path
        STEP_LOG_PATH = self.step_log_path

        common.print_msg("配置文件读取完成")

    def main(self):
        global TOTAL_IMAGE_COUNT
        global THREAD_COUNT

        start_time = time.time()

        # 图片保存目录
        print_step_msg("创建图片根目录：" + IMAGE_DOWNLOAD_PATH)
        if not common.make_dir(IMAGE_DOWNLOAD_PATH, 2):
            print_error_msg("创建图片根目录：" + IMAGE_DOWNLOAD_PATH + " 失败，程序结束！")
            common.process_exit()

        # 设置代理
        if self.is_proxy == 1 or self.is_proxy == 2:
            common.set_proxy(self.proxy_ip, self.proxy_port, "https")

        # 寻找idlist，如果没有结束进程
        user_id_list = {}
        if os.path.exists(self.user_id_list_file_path):
            user_id_list_file = open(self.user_id_list_file_path, "r")
            all_user_list = user_id_list_file.readlines()
            user_id_list_file.close()
            for user_info in all_user_list:
                if len(user_info) < 3:
                    continue
                user_info = user_info.replace("\xef\xbb\xbf", "").replace(" ", "").replace("\n", "").replace("\r", "")
                user_info_list = user_info.split("\t")

                user_account = user_info_list[0]
                user_id_list[user_account] = user_info_list
                # 如果没有数量，则为0
                if len(user_id_list[user_account]) < 2:
                    user_id_list[user_account].append("0")
                if user_id_list[user_account][1] == '':
                    user_id_list[user_account][1] = '0'
                # 处理上一次图片的上传时间
                if len(user_id_list[user_account]) < 3:
                    user_id_list[user_account].append("")
                if user_id_list[user_account][2] == '':
                    user_id_list[user_account][2] = '0'

        else:
            print_error_msg("用户ID存档文件: " + self.user_id_list_file_path + "不存在，程序结束！")
            common.process_exit()

        # 创建临时存档文件
        new_user_id_list_file = open(NEW_USER_ID_LIST_FILE_PATH, "w")
        new_user_id_list_file.close()

        TOTAL_IMAGE_COUNT = 0

        # 循环下载每个id
        for user_account in sorted(user_id_list.keys()):
            # 检查正在运行的线程数
            while THREAD_COUNT >= self.thread_count:
                time.sleep(10)

            # 线程数+1
            threadLock.acquire()
            THREAD_COUNT += 1
            threadLock.release()

            # 开始下载
            thread = Download(user_id_list[user_account])
            thread.start()

            time.sleep(1)

        # 检查所有线程是不是全部结束了
        while THREAD_COUNT != 0:
            time.sleep(10)

        # 删除临时文件夹
        common.remove_dir(IMAGE_TEMP_PATH)

        # 重新排序保存存档文件
        new_user_id_list_file = open(NEW_USER_ID_LIST_FILE_PATH, "r")
        all_user_list = new_user_id_list_file.readlines()
        new_user_id_list_file.close()
        user_id_list = {}
        for user_info in all_user_list:
            if len(user_info) < 5:
                continue
            user_info = user_info.replace("\xef\xbb\xbf", "").replace("\n", "").replace("\r", "")
            user_info_list = user_info.split("\t")
            user_id_list[user_info_list[0]] = user_info_list
        new_user_id_list_file = open(NEW_USER_ID_LIST_FILE_PATH, "w")
        for user_id in sorted(user_id_list.keys()):
            new_user_id_list_file.write("\t".join(user_id_list[user_id]) + "\n")
        new_user_id_list_file.close()

        stop_time = time.time()
        print_step_msg("存档文件中所有用户图片已成功下载，耗时" + str(int(stop_time - start_time)) + "秒，共计图片" + str(TOTAL_IMAGE_COUNT) + "张")


class Download(threading.Thread):

    def __init__(self, user_info):
        threading.Thread.__init__(self)
        self.user_info = user_info

    # 返回的是当前时区对应的时间
    def get_image_last_modified(self, info):
        last_modified_time = common.get_response_info(info, 'last-modified')
        last_modified_time = time.strptime(last_modified_time, '%a, %d %b %Y %H:%M:%S %Z')
        return int(time.mktime(last_modified_time)) - time.timezone

    def save_image(self, image_byte, image_path):
        image_path = common.change_path_encoding(image_path)
        image_file = open(image_path, "wb")
        image_file.write(image_byte)
        image_file.close()

    def run(self):
        global INIT_MAX_ID
        global GET_IMAGE_COUNT
        global IMAGE_TEMP_PATH
        global IMAGE_DOWNLOAD_PATH
        global NEW_USER_ID_LIST_FILE_PATH
        global TOTAL_IMAGE_COUNT
        global THREAD_COUNT

        user_account = self.user_info[0]

        try:
            print_step_msg(user_account + " 开始")

            # 初始化数据
            last_image_time = self.user_info[2]
            self.user_info[2] = '0'  # 置空，存放此次的最后图片上传时间
            data_tweet_id = INIT_MAX_ID
            image_count = 1
            image_url_list = []
            is_over = False
            # 如果有存档记录，则直到找到在记录之前的图片，否则都算错误
            if last_image_time == '0':
                is_error = False
            else:
                is_error = True

            # 如果需要重新排序则使用临时文件夹，否则直接下载到目标目录
            if IS_SORT == 1:
                image_path = IMAGE_TEMP_PATH + "\\" + user_account
            else:
                image_path = IMAGE_DOWNLOAD_PATH + "\\" + user_account
            if not common.make_dir(image_path, 1):
                print_error_msg(user_account + " 创建图片下载目录： " + image_path + " 失败，程序结束！")
                common.process_exit()

            # 图片下载
            while 1:
                photo_page_url = "https://twitter.com/i/profiles/show/%s/media_timeline?include_available_features=1&include_entities=1&max_position=%s" % (user_account, data_tweet_id)
                [photo_page_return_code, photo_page_data] = common.http_request(photo_page_url)
                if photo_page_return_code != 1:
                    print_error_msg(user_account + " 无法获取相册信息: " + photo_page_url)
                    break
                try:
                    page = json.read(photo_page_data)
                except:
                    print_error_msg(user_account + " 返回信息：" + str(photo_page_data) + " 不是一个JSON数据")
                    break

                if not isinstance(page, dict):
                    print_error_msg(user_account + " JSON数据：" + str(page) + " 不是一个字典")
                    break
                if 'has_more_items' not in page:
                    print_error_msg(user_account + " 在JSON数据：" + str(page) + " 中没有找到'has_more_items'字段")
                    break
                if 'items_html' not in page:
                    print_error_msg(user_account + " 在JSON数据：" + str(page) + " 中没有找到'items_html'字段")
                    break
                if 'min_position' not in page:
                    print_error_msg(user_account + " 在JSON数据：" + str(page) + " 中没有找到'min_position'字段")
                    break

                # 正则表达，匹配data-image-url="XXX"
                urls = re.findall('data-image-url="([^"]*)"', page['items_html'])
                for image_url in urls:
                    image_url = str(image_url)
                    image_url_list.append(image_url)
                    trace(user_account + " image URL:" + image_url)

                    [[image_response_return_code, image_response_data], image_response_info] = common.http_request(image_url, None, True)
                    # 404，不算做错误，图片已经被删掉了
                    if image_response_return_code == -1:
                        pass
                    elif image_response_return_code == 1:
                        image_time = self.get_image_last_modified(image_response_info)
                        # 将第一张image的URL保存到新id list中
                        if self.user_info[2] == "0":
                            self.user_info[2] = str(image_time)

                        # 检查是否已下载到前一次的图片
                        if int(last_image_time) > 0 and image_time <= int(last_image_time):
                            is_over = True
                            is_error = False
                            break

                        # 文件类型
                        file_type = image_url.split(".")[-1].split(':')[0]
                        file_path = image_path + "\\" + str("%04d" % image_count) + "." + file_type

                        print_step_msg(user_account + " 开始下载第 " + str(image_count) + "张图片：" + image_url)
                        self.save_image(image_response_data, file_path)
                        print_step_msg(user_account + " 第" + str(image_count) + "张图片下载成功")
                        image_count += 1
                    else:
                        print_error_msg(user_account + " 第" + str(image_count) + "张图片 " + image_url + " 获取失败")

                    # 达到配置文件中的下载数量，结束
                    if GET_IMAGE_COUNT > 0 and image_count > GET_IMAGE_COUNT:
                        is_over = True
                        is_error = False
                        break

                if is_over:
                    break

                if page['has_more_items'] and 'min_position' in page:
                    # 设置最后一张的data-tweet-id
                    data_tweet_id = page['min_position']
                else:
                    break

            TOTAL_IMAGE_COUNT += image_count - 1

            print_step_msg(user_account + " 下载完毕，总共获得" + str(image_count - 1) + "张图片")

            # 排序
            if IS_SORT == 1:
                image_list = sorted(os.listdir(image_path), reverse=True)
                # 判断排序目标文件夹是否存在
                if len(image_list) >= 1:
                    destination_path = IMAGE_DOWNLOAD_PATH + "\\" + user_account
                    if not common.make_dir(destination_path, 1):
                        print_error_msg(user_account + " 创建图片子目录： " + destination_path + " 失败，程序结束！")
                        common.process_exit()

                    # 倒叙排列
                    count = int(self.user_info[1])

                    for file_name in image_list:
                        count += 1
                        file_type = file_name.split(".")[1]
                        common.copy_files(image_path + "\\" + file_name, destination_path + "\\" + str("%04d" % count) + "." + file_type)

                    print_step_msg(user_account + " 图片从下载目录移动到保存目录成功")

                # 删除临时文件夹
                common.remove_dir(image_path)

            self.user_info[1] = str(int(self.user_info[1]) + image_count - 1)

            if is_error:
                print_error_msg(user_account + " 图片数量异常，请手动检查")

            # 保存最后的信息
            threadLock.acquire()
            new_user_id_list_file = open(NEW_USER_ID_LIST_FILE_PATH, "a")
            new_user_id_list_file.write("\t".join(self.user_info) + "\n")
            new_user_id_list_file.close()
            TOTAL_IMAGE_COUNT += image_count - 1
            THREAD_COUNT -= 1
            threadLock.release()

            print_step_msg(user_account + " 完成")
        except Exception, e:
            print_step_msg(user_account + " 异常")
            print_error_msg(str(e))

if __name__ == "__main__":
    Twitter(os.getcwd() + "\\info\\idlist_1.txt", os.getcwd() + "\\photo\\twitter1", os.getcwd() + "\\photo\\twitter1\\tempImage").main()
    Twitter(os.getcwd() + "\\info\\idlist_2.txt", os.getcwd() + "\\photo\\twitter2", os.getcwd() + "\\photo\\twitter2\\tempImage").main()
    Twitter(os.getcwd() + "\\info\\idlist_3.txt", os.getcwd() + "\\photo\\twitter3", os.getcwd() + "\\photo\\twitter3\\tempImage").main()
