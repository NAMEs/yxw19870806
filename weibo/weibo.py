# -*- coding:UTF-8  -*-
'''
Created on 2013-8-28

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
如有问题或建议请联系
'''

from common import robot, tool, json
import hashlib
# import multiprocessing
import os
import random
import threading
import time

IS_TRACE = False
IS_SHOW_ERROR = False
IS_SHOW_STEP = False
TRACE_LOG_PATH = ""
ERROR_LOG_PATH = ""
STEP_LOG_PATH = ""

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


def visit_weibo(url):
    [temp_page_return_code, temp_page] = tool.http_request(url)[:2]
    if temp_page_return_code == 1:
        # 有重定向
        redirect_url_index = temp_page.find("location.replace")
        if redirect_url_index != -1:
            redirect_url_start = temp_page.find("'", redirect_url_index) + 1
            redirect_url_stop = temp_page.find("'", redirect_url_start)
            redirect_url = temp_page[redirect_url_start:redirect_url_stop]
            return visit_weibo(redirect_url)
        # 没有cookies无法访问的处理
        if temp_page.find("用户名或密码错误") != -1:
            print_error_msg("登陆状态异常，请在浏览器中重新登陆微博账号")
            tool.process_exit()
        else:
            try:
                temp_page = temp_page.decode("utf-8")
                if temp_page.find("用户名或密码错误") != -1:
                    print_error_msg("登陆状态异常，请在浏览器中重新登陆微博账号")
                    tool.process_exit()
            except:
                pass
        # 返回页面
        return str(temp_page)
    return False


class Weibo(robot.Robot):

    def __init__(self, save_data_path="", this_image_download_path="", this_image_temp_path=""):
        global IMAGE_COUNT_PER_PAGE
        global GET_IMAGE_COUNT
        global IMAGE_TEMP_PATH
        global IMAGE_DOWNLOAD_PATH
        global NEW_SAVE_DATA_PATH
        global IS_SORT
        global IS_TRACE
        global IS_SHOW_ERROR
        global IS_SHOW_STEP
        global TRACE_LOG_PATH
        global ERROR_LOG_PATH
        global STEP_LOG_PATH

        # multiprocessing.Process.__init__(self)
        robot.Robot.__init__(self)

        if save_data_path != "":
            self.save_data_path = save_data_path

        IMAGE_COUNT_PER_PAGE = 20  # 每次请求获取的图片数量
        GET_IMAGE_COUNT = self.get_image_count
        if this_image_temp_path != "":
            IMAGE_TEMP_PATH = this_image_temp_path
        else:
            IMAGE_TEMP_PATH = self.image_temp_path
        if this_image_download_path != "":
            IMAGE_DOWNLOAD_PATH = this_image_download_path
        else:
            IMAGE_DOWNLOAD_PATH = self.image_download_path
        IS_SORT = self.is_sort
        IS_TRACE = self.is_trace
        IS_SHOW_ERROR = self.is_show_error
        IS_SHOW_STEP = self.is_show_step
        NEW_SAVE_DATA_PATH = os.path.join(os.path.abspath(""), "info", time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.basename(self.save_data_path))
        TRACE_LOG_PATH = self.trace_log_path
        ERROR_LOG_PATH = self.error_log_path
        STEP_LOG_PATH = self.step_log_path

        tool.print_msg("配置文件读取完成")

    def main(self):
        global TOTAL_IMAGE_COUNT

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

        # 寻找存档，如果没有结束进程
        user_id_list = {}
        if os.path.exists(self.save_data_path):
            save_data_file = open(self.save_data_path, "r")
            all_user_list = save_data_file.readlines()
            save_data_file.close()
            for user_info in all_user_list:
                if len(user_info) < 5:
                    continue
                user_info = user_info.replace("\xef\xbb\xbf", "").replace("\n", "").replace("\r", "")
                user_info_list = user_info.split("\t")

                user_id = user_info_list[0]
                user_id_list[user_id] = user_info_list
                # 如果没有名字，则名字用uid代替
                if len(user_id_list[user_id]) < 2:
                    user_id_list[user_id].append(user_id)
                if user_id_list[user_id][1] == "":
                    user_id_list[user_id][1] = user_id
                # 如果没有数量，则为0
                if len(user_id_list[user_id]) < 3:
                    user_id_list[user_id].append("0")
                if user_id_list[user_id][2] == "":
                    user_id_list[user_id][2] = "0"
                # 处理上一次图片的上传时间
                if len(user_id_list[user_id]) < 4:
                    user_id_list[user_id].append("0")
                if user_id_list[user_id][3] == "":
                    user_id_list[user_id][3] = "0"
        else:
            print_error_msg("存档文件：" + self.save_data_path + "不存在，程序结束！")
            tool.process_exit()

        # 创建临时存档文件
        new_save_data_file = open(NEW_SAVE_DATA_PATH, "w")
        new_save_data_file.close()

        # 先访问下页面，产生个cookies
        visit_weibo("http://photo.weibo.com/photos/get_all?uid=1263970750&count=30&page=1&type=3")
        time.sleep(2)

        TOTAL_IMAGE_COUNT = 0

        # 启用线程监控是否需要暂停其他下载线程
        process_control_thread = tool.ProcessControl()
        process_control_thread.setDaemon(True)
        process_control_thread.start()

        # 循环下载每个id
        main_thread_count = threading.activeCount()
        for user_id in sorted(user_id_list.keys()):
            # 检查正在运行的线程数
            while threading.activeCount() >= self.thread_count + main_thread_count:
                time.sleep(10)

            # 开始下载
            thread = Download(user_id_list[user_id])
            thread.start()

            time.sleep(1)

        # 检查除主线程外的其他所有线程是不是全部结束了
        while threading.activeCount() > main_thread_count:
            time.sleep(10)

        # 删除临时文件夹
        tool.remove_dir(IMAGE_TEMP_PATH)

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

        duration_time = int(time.time() - start_time)
        print_step_msg("全部下载完毕，耗时" + str(duration_time) + "秒，共计图片" + str(TOTAL_IMAGE_COUNT) + "张")


class Download(threading.Thread):

    def __init__(self, user_info):
        threading.Thread.__init__(self)
        self.user_info = user_info

    def run(self):
        global IMAGE_COUNT_PER_PAGE
        global GET_IMAGE_COUNT
        global IMAGE_TEMP_PATH
        global IMAGE_DOWNLOAD_PATH
        global NEW_SAVE_DATA_PATH
        global TOTAL_IMAGE_COUNT

        user_id = self.user_info[0]
        user_name = self.user_info[1]

        try:
            print_step_msg(user_name + " 开始")

            # 初始化数据
            last_image_time = self.user_info[3]
            self.user_info[3] = "0"  # 置空，存放此次的最后图片上传时间
            page_count = 1
            image_count = 1
            is_over = False
            # 如果有存档记录，则直到找到在记录之前的图片，否则都算错误
            if last_image_time == "0":
                is_error = False
            else:
                is_error = True

            # 如果需要重新排序则使用临时文件夹，否则直接下载到目标目录
            if IS_SORT == 1:
                image_path = os.path.join(IMAGE_TEMP_PATH, user_name)
            else:
                image_path = os.path.join(IMAGE_DOWNLOAD_PATH, user_name)
            if not tool.make_dir(image_path, 1):
                print_error_msg(user_name + " 创建图片下载目录：" + image_path + " 失败，程序结束！")
                tool.process_exit()

            # 日志文件插入信息
            while 1:
                photo_album_url = "http://photo.weibo.com/photos/get_all?uid=%s&count=%s&page=%s&type=3" % (user_id, IMAGE_COUNT_PER_PAGE, page_count)
                trace("相册专辑地址：" + photo_album_url)
                photo_page_data = visit_weibo(photo_album_url)
                trace("返回JSON数据：" + str(photo_page_data))
                try:
                    page = json.read(photo_page_data)
                except:
                    print_error_msg(user_name + " 返回信息不是一个JSON数据")
                    break

                # 总的图片数
                try:
                    total_image_count = page["data"]["total"]
                except:
                    print_error_msg(user_name + " 在JSON数据：" + str(page) + " 中没有找到'total'字段")
                    break

                try:
                    photo_list = page["data"]["photo_list"]
                except:
                    print_error_msg(user_name + " 在JSON数据：" + str(page) + " 中没有找到'total'字段" )
                    break

                for image_info in photo_list:
                    if not isinstance(image_info, dict):
                        print_error_msg(user_name + " JSON数据['photo_list']：" + str(image_info) + " 不是一个字典")
                        continue
                    if ("pic_name" and "timestamp") in image_info:
                        # 将第一张image的时间戳保存到新id list中
                        if self.user_info[3] == "0":
                            self.user_info[3] = str(image_info["timestamp"])
                        # 检查是否图片时间小于上次的记录
                        if 0 < int(last_image_time) >= int(image_info["timestamp"]):
                            is_over = True
                            is_error = False
                            break

                        if "pic_host" in image_info:
                            image_host = image_info["pic_host"]
                        else:
                            image_host = ""
                        for try_count in range(1, 6):
                            if image_host == "":
                                image_host = "http://ww%s.sinaimg.cn" % str(random.randint(1, 4))
                            image_url = image_host + "/large/" + image_info["pic_name"]
                            if try_count == 1:
                                print_step_msg(user_name + " 开始下载第" + str(image_count) + "张图片：" + image_url)
                            else:
                                print_step_msg(user_name + " 重试下载第" + str(image_count) + "张图片：" + image_url)
                            [image_return_code, image_byte] = tool.http_request(image_url)[:2]
                            if image_return_code == 1:
                                md5 = hashlib.md5()
                                md5.update(image_byte)
                                md5_digest = md5.hexdigest()
                                # 处理获取的文件为weibo默认获取失败的图片
                                if md5_digest not in ["d29352f3e0f276baaf97740d170467d7", "7bd88df2b5be33e1a79ac91e7d0376b5"]:
                                    file_type = image_url.split(".")[-1]
                                    if file_type.find("/") != -1:
                                        file_type = "jpg"
                                    file_path = os.path.join(image_path, str("%04d" % image_count) + "." + file_type)
                                    file_path = tool.change_path_encoding(file_path)
                                    image_file = open(file_path, "wb")
                                    image_file.write(image_byte)
                                    image_file.close()
                                    image_count += 1
                                    print_step_msg(user_name + " 第" + str(image_count) + "张图片下载成功")
                                    break
                            if try_count == 5:
                                print_error_msg(user_name + " 第" + str(image_count) + "张图片 " + image_url + " 下载失败")
                            image_host = ""
                    else:
                        print_error_msg(user_name + " 在JSON数据：" + str(image_info) + " 中没有找到'pic_name'或'timestamp'字段")

                    # 达到配置文件中的下载数量，结束
                    if 0 < GET_IMAGE_COUNT < image_count:
                        is_over = True
                        break

                if is_over:
                    break

                if (total_image_count / IMAGE_COUNT_PER_PAGE) > (page_count - 1):
                    page_count += 1
                else:
                    # 全部图片下载完毕
                    break

            # 如果有错误且没有发现新的图片，复原旧数据
            if self.user_info[3] == "0" and last_image_time != "0":
                self.user_info[3] = last_image_time

            print_step_msg(user_name + " 下载完毕，总共获得" + str(image_count - 1) + "张图片")

            # 排序
            if IS_SORT == 1:
                destination_path = os.path.join(IMAGE_DOWNLOAD_PATH, user_name)
                if robot.sort_file(image_path, destination_path, int(self.user_info[2]), 4):
                    print_step_msg(user_name + " 图片从下载目录移动到保存目录成功")
                else:
                    print_error_msg(user_name + " 创建图片子目录： " + destination_path + " 失败，程序结束！")
                    tool.process_exit()
            self.user_info[2] = str(int(self.user_info[2]) + image_count - 1)
            if is_error:
                print_error_msg(user_name + " 图片数量异常，请手动检查")

            # 保存最后的信息
            threadLock.acquire()
            new_save_data_file = open(NEW_SAVE_DATA_PATH, "a")
            new_save_data_file.write("\t".join(self.user_info) + "\n")
            new_save_data_file.close()
            TOTAL_IMAGE_COUNT += image_count - 1
            threadLock.release()

            print_step_msg(user_name + " 完成")
        except Exception, e:
            print_step_msg(user_name + " 异常")
            print_error_msg(str(e))


if __name__ == "__main__":
    for id in ["ATF", "lunar", "save_1", "save_2", "snh48"]:
        save_file_name = "info\\%s.data" % id
        image_download_dir_name = "photo\\%s" % id
        save_file_path = os.path.join(os.path.abspath(""), save_file_name)
        image_download_path = os.path.join(os.path.abspath(""), image_download_dir_name)
        image_temp_path = os.path.join(image_download_path, "tempImage")
        Weibo(save_file_path, image_download_path, image_temp_path).main()
