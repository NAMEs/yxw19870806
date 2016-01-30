# -*- coding:UTF-8  -*-
'''
Created on 2015-6-23

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
如有问题或建议请联系
'''

from common import robot, tool
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
    tool.trace(msg, IS_TRACE, TRACE_LOG_PATH)
    threadLock.release()


def print_error_msg(msg):
    threadLock.acquire()
    tool.print_error_msg(msg, IS_SHOW_ERROR, ERROR_LOG_PATH)
    threadLock.release()


def print_step_msg(msg):
    threadLock.acquire()
    tool.print_step_msg(msg, IS_SHOW_STEP, STEP_LOG_PATH)
    threadLock.release()


class Bcy(robot.Robot):

    def __init__(self):
        global GET_IMAGE_COUNT
        global IMAGE_DOWNLOAD_PATH
        global NEW_SAVE_DATA_PATH
        global IS_SORT
        global IS_TRACE
        global IS_SHOW_ERROR
        global IS_SHOW_STEP
        global TRACE_LOG_PATH
        global ERROR_LOG_PATH
        global STEP_LOG_PATH

        super(Bcy, self).__init__()

        # 全局变量
        GET_IMAGE_COUNT = self.get_image_count
        IMAGE_DOWNLOAD_PATH = self.image_download_path
        IS_SORT = self.is_sort
        IS_TRACE = self.is_trace
        IS_SHOW_ERROR = self.is_show_error
        IS_SHOW_STEP = self.is_show_step
        NEW_SAVE_DATA_PATH = os.getcwd() + "\\info\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(self.save_data_path)[-1]
        TRACE_LOG_PATH = self.trace_log_path
        ERROR_LOG_PATH = self.error_log_path
        STEP_LOG_PATH = self.step_log_path

        tool.print_msg("配置文件读取完成")

    def main(self):
        global TOTAL_IMAGE_COUNT
        global THREAD_COUNT

        start_time = time.time()

        # 图片保存目录
        print_step_msg("创建图片根目录：" + IMAGE_DOWNLOAD_PATH)
        if not tool.make_dir(IMAGE_DOWNLOAD_PATH, 2):
            print_error_msg("创建图片根目录：" + IMAGE_DOWNLOAD_PATH + " 失败，程序结束！")
            tool.process_exit()

        # 设置代理
        if self.is_proxy == 1:
            tool.set_proxy(self.proxy_ip, self.proxy_port, "http")

        # 设置系统cookies
        if not tool.set_cookie(self.cookie_path, self.browser_version):
            print_error_msg("导入浏览器cookies失败，程序结束！")
            tool.process_exit()

        # 寻找idlist，如果没有结束进程
        user_id_list = {}
        if os.path.exists(self.save_data_path):
            save_data_file = open(self.save_data_path, "r")
            all_user_list = save_data_file.readlines()
            save_data_file.close()
            for user_info in all_user_list:
                if len(user_info) < 3:
                    continue
                user_info = user_info.replace("\xef\xbb\xbf", "").replace(" ", "").replace("\n", "").replace("\r", "")
                user_info_list = user_info.split("\t")

                user_id = user_info_list[0]
                user_id_list[user_id] = user_info_list
                # 如果没有数量，则为0
                if len(user_id_list[user_id]) < 2:
                    user_id_list[user_id].append("0")
                if user_id_list[user_id][1] == '':
                    user_id_list[user_id][1] = '0'
                # 处理上一次rp id
                if len(user_id_list[user_id]) < 3:
                    user_id_list[user_id].append("")
                if user_id_list[user_id][2] == '':
                    user_id_list[user_id][2] = '0'
        else:
            print_error_msg("用户ID存档文件: " + self.save_data_path + "不存在，程序结束！")
            tool.process_exit()

        # 创建临时存档文件
        new_save_data_file = open(NEW_SAVE_DATA_PATH, "w")
        new_save_data_file.close()

        TOTAL_IMAGE_COUNT = 0
        # 循环下载每个id
        for user_id in sorted(user_id_list.keys()):
            # 检查正在运行的线程数
            while THREAD_COUNT >= self.thread_count:
                time.sleep(10)

            # 线程数+1
            threadLock.acquire()
            THREAD_COUNT += 1
            threadLock.release()

            # 开始下载
            thread = Download(user_id_list[user_id])
            thread.start()

            time.sleep(1)

        # 检查所有线程是不是全部结束了
        while THREAD_COUNT != 0:
            time.sleep(10)

        # 重新排序保存存档文件
        new_save_data_file = open(NEW_SAVE_DATA_PATH, "r")
        all_user_list = new_save_data_file.readlines()
        new_save_data_file.close()
        user_id_list = {}
        for user_info in all_user_list:
            if len(user_info) < 5:
                continue
            user_info = user_info.replace("\xef\xbb\xbf", "").replace("\n", "").replace("\r", "")
            user_info_list = user_info.split("\t")
            user_id_list[user_info_list[0]] = user_info_list
        new_save_data_file = open(NEW_SAVE_DATA_PATH, "w")
        for user_id in sorted(user_id_list.keys()):
            new_save_data_file.write("\t".join(user_id_list[user_id]) + "\n")
        new_save_data_file.close()

        stop_time = time.time()
        print_step_msg("存档文件中所有用户图片已成功下载，耗时" + str(int(stop_time - start_time)) + "秒，共计图片" + str(TOTAL_IMAGE_COUNT) + "张")


class Download(threading.Thread):

    def __init__(self, user_info):
        threading.Thread.__init__(self)
        self.user_info = user_info

    def run(self):
        global GET_IMAGE_COUNT
        global IMAGE_DOWNLOAD_PATH
        global NEW_SAVE_DATA_PATH
        global IS_SORT
        global TOTAL_IMAGE_COUNT
        global THREAD_COUNT

        coser_id = self.user_info[0]
        cn = self.user_info[1]

        try:
            print_step_msg(cn + " 开始")

            last_rp_id = self.user_info[2]
            self.user_info[2] = ''  # 置空，存放此次的最后rp id
            this_cn_total_image_count = 0
            page_count = 1
            max_page_count = -1
            need_make_download_dir = True  # 是否需要创建cn目录
            rp_id_list = []
            is_over = False
            # 如果有存档记录，则直到找到与前一次一致的地址，否则都算有异常
            if last_rp_id != '0':
                is_error = True
            else:
                is_error = False

            while 1:
                photo_album_url = 'http://bcy.net/u/%s/post/cos?&p=%s' % (coser_id, page_count)
                [photo_album_page_return_code, photo_album_page] = tool.http_request(photo_album_url)[:2]
                if photo_album_page_return_code != 1:
                    print_error_msg(cn + " 无法获取数据: " + photo_album_url)
                    break

                rp_id_result_list = re.findall('/coser/detail/(\d+)/(\d+)"', photo_album_page)
                title_result_list = re.findall('<img src="\S*" alt="([\S ]*)" />', photo_album_page)
                if '${post.title}' in title_result_list:
                    title_result_list.remove('${post.title}')
                if len(rp_id_result_list) != len(title_result_list):
                    print_error_msg(cn + " 第" + str(page_count) + "页获取的rp_id和title数量不符")
                    break

                title_index = 0
                for data in rp_id_result_list:
                    cp_id = data[0]
                    rp_id = data[1]
                    rp_id_list.append(rp_id)

                    if self.user_info[2] == '':
                        self.user_info[2] = rp_id
                    # 检查是否已下载到前一次的图片
                    if int(rp_id) <= int(last_rp_id):
                        is_over = True
                        is_error = False
                        break

                    print_step_msg("rp: " + rp_id)

                    # CN目录
                    image_path = IMAGE_DOWNLOAD_PATH + "\\" + cn

                    if need_make_download_dir:
                        if not tool.make_dir(image_path, 1):
                            print_error_msg(cn + " 创建CN目录： " + image_path + " 失败，程序结束！")
                            tool.process_exit()
                        need_make_download_dir = False

                    # 正片目录
                    title = title_result_list[title_index]
                    # 过滤一些windows文件名屏蔽的字符
                    for filter in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                        title = title.replace(filter, ' ')
                    # 去除前后空格
                    title = title.strip()
                    if title != '':
                        rp_path = image_path + "\\" + rp_id + ' ' + title
                    else:
                        rp_path = image_path + "\\" + rp_id
                    if not tool.make_dir(rp_path, 1):
                        # 目录出错，把title去掉后再试一次，如果还不行退出
                        print_error_msg(cn + " 创建正片目录： " + rp_path + " 失败，尝试不使用title！")
                        rp_path = image_path + "\\" + rp_id
                        if not tool.make_dir(rp_path, 1):
                            print_error_msg(cn + " 创建正片目录： " + rp_path + " 失败，程序结束！")
                            tool.process_exit()

                    rp_url = 'http://bcy.net/coser/detail/%s/%s' % (cp_id, rp_id)
                    [rp_page_return_code, rp_page] = tool.http_request(rp_url)[:2]
                    if rp_page_return_code == 1:
                        image_count = 0
                        image_index = rp_page.find("src='")
                        while image_index != -1:
                            image_count += 1

                            image_start = rp_page.find("http", image_index)
                            image_stop = rp_page.find("'", image_start)
                            image_url = rp_page[image_start:image_stop]
                            # 禁用指定分辨率
                            image_url = "/".join(image_url.split("/")[0:-1])

                            if image_url.rfind('/') < image_url.rfind('.'):
                                file_type = image_url.split(".")[-1]
                            else:
                                file_type = 'jpg'
                            file_path = rp_path + "\\" + str("%03d" % image_count) + "." + file_type

                            print_step_msg(cn + ":" + rp_id + " 开始下载第" + str(image_count) + "张图片：" + image_url)
                            if tool.save_image(image_url, file_path):
                                print_step_msg(cn + ":" + rp_id + " 第" + str(image_count) + "张图片下载成功")
                            else:
                                print_error_msg(cn + ":" + rp_id + " 第" + str(image_count) + "张图片 " + image_url + " 下载失败")

                            image_index = rp_page.find("src='", image_index + 1)

                        if image_count == 0:
                            print_error_msg(cn + " " + rp_id + " 没有任何图片")

                        this_cn_total_image_count += image_count - 1

                    title_index += 1

                if is_over:
                    break

                # 看看总共有几页
                if max_page_count == -1:
                    max_page_count_result = re.findall(r'<a href="/u/'+ coser_id + '/post/cos\?&p=(\d*)">尾页</a>', photo_album_page)
                    if len(max_page_count_result) > 0:
                        max_page_count = int(max_page_count_result[0])
                    else:
                        max_page_count = 1

                if page_count >= max_page_count:
                    break

                page_count += 1

            print_step_msg(cn + " 下载完毕，总共获得" + str(this_cn_total_image_count) + "张图片")

            if is_error:
                print_error_msg(cn + " 图片数量异常，请手动检查")

            # 保存最后的信息
            threadLock.acquire()
            new_save_data_file = open(NEW_SAVE_DATA_PATH, "a")
            new_save_data_file.write("\t".join(self.user_info) + "\n")
            new_save_data_file.close()
            TOTAL_IMAGE_COUNT += this_cn_total_image_count
            threadLock.release()

            print_step_msg(cn + " 完成")
        except Exception, e:
            print_step_msg(cn + " 异常")
            print_error_msg(str(e))

        THREAD_COUNT -= 1

if __name__ == "__main__":
    Bcy().main()
