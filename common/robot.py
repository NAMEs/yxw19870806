# -*- coding:UTF-8  -*-

import tool
import os
import traceback


class Robot(object):

    def __init__(self):

        config = analyze_config(os.path.join(os.path.abspath(''), "..\\common\\config.ini"))

        # 日志
        self.is_log = get_config(config, "IS_LOG", 1, 2)
        self.is_show_error = get_config(config, "IS_SHOW_ERROR", 1, 2)
        self.is_trace = get_config(config, "IS_TRACE", 1, 2)
        self.is_show_step = get_config(config, "IS_SHOW_STEP", 1, 2)
        if self.is_log == 0:
            self.trace_log_path = ""
            self.step_log_path = ""
        else:
            self.trace_log_path = get_config(config, "TRACE_LOG_PATH", "log/traceLog.txt", 3)
            self.step_log_path = get_config(config, "STEP_LOG_PATH", "log/stepLog.txt", 3)
            # 日志文件保存目录
            step_log_dir = os.path.dirname(self.step_log_path)
            if not tool.make_dir(step_log_dir, 0):
                tool.print_error_msg("创建步骤日志目录：" + step_log_dir + " 失败，程序结束！", self.is_show_step, self.step_log_path)
                tool.process_exit()
            trace_log_dir = os.path.dirname(self.trace_log_path)
            if not tool.make_dir(trace_log_dir, 0):
                tool.print_error_msg("创建调试日志目录：" + trace_log_dir + " 失败，程序结束！", self.is_show_step, self.trace_log_path)
                tool.process_exit()
        self.error_log_path = get_config(config, "ERROR_LOG_FILE_NAME", "log/errorLog.txt", 3)
        error_log_dir = os.path.dirname(self.error_log_path)
        if not tool.make_dir(error_log_dir, 0):
            tool.print_error_msg("创建错误日志目录：" + error_log_dir + " 失败，程序结束！", self.is_show_error, self.error_log_path)
            tool.process_exit()

        # 存档
        self.image_download_path = get_config(config, "IMAGE_DOWNLOAD_PATH", "photo", 3)
        self.image_temp_path = get_config(config, "IMAGE_TEMP_PATH", "tempImage", 3)

        self.is_sort = get_config(config, "IS_SORT", 1, 2)
        self.get_image_count = get_config(config, "GET_IMAGE_COUNT", 0, 2)

        self.save_data_path = get_config(config, "SAVE_DATA_PATH", "info/save.data", 3)

        # 代理
        self.is_proxy = get_config(config, "IS_PROXY", 2, 2)
        self.proxy_ip = get_config(config, "PROXY_IP", "127.0.0.1", 0)
        self.proxy_port = get_config(config, "PROXY_PORT", "8087", 0)

        # 操作系统&浏览器
        self.browser_version = get_config(config, "BROWSER_VERSION", 2, 2)

        # cookie
        is_auto_get_cookie = get_config(config, "IS_AUTO_GET_COOKIE", 1, 2)
        if is_auto_get_cookie == 0:
            self.cookie_path = get_config(config, "COOKIE_PATH", "", 0)
        else:
            self.cookie_path = tool.get_default_browser_cookie_path(self.browser_version)

        # 线程数
        self.thread_count = get_config(config, "THREAD_COUNT", 10, 2)


# 获取配置文件
# config : 字典格式，如：{key1:value1, key2:value2}
# mode=0 : 直接赋值
# mode=1 : 字符串拼接
# mode=2 : 取整
# mode=3 : 文件路径，以'\'开头的为当前目录下创建
# prefix: 前缀，只有在mode=1时有效
# postfix: 后缀，只有在mode=1时有效
def get_config(config, key, default_value, mode, prefix=None, postfix=None):
    value = None
    if key in config:
        if mode == 0:
            value = config[key]
        elif mode == 1:
            value = config[key]
            if prefix is not None:
                value = prefix + value
            if postfix is not None:
                value = value + postfix
        elif mode == 2:
            try:
                value = int(config[key])
            except:
                tool.print_msg("配置文件config.ini中key为'" + key + "'的值必须是一个整数，使用程序默认设置")
                traceback.print_exc()
                value = default_value
        elif mode == 3:
            value = config[key]
            if value[0] == '\\':
                value = os.path.join(os.path.abspath(''), value[1:])  # 第一个 \ 仅做标记使用，实际需要去除
    else:
        tool.print_msg("配置文件config.ini中没有找到key为'" + key + "'的参数，使用程序默认设置")
        value = default_value
    return value


def analyze_config(config_path):
    config_file = open(config_path, 'r')
    lines = config_file.readlines()
    config_file.close()
    config = {}
    for line in lines:
        if len(line) == 0:
            continue
        line = line.lstrip().rstrip().replace(" ", "")
        if len(line) > 1 and line[0] != "#" and line.find('=') >= 0:
            try:
                line = line.split("=")
                config[line[0]] = line[1]
            except Exception, e:
                tool.print_msg(str(e))
                pass
    return config


def sort_file(source_path, destination_path, start_count, file_name_length):
    image_list = tool.get_dir_files_name(source_path, 'desc')
    # 判断排序目标文件夹是否存在
    if len(image_list) >= 1:
        if not tool.make_dir(destination_path, 1):
            return False
        # 倒叙排列
        for file_name in image_list:
            start_count += 1
            file_type = os.path.splitext(file_name)[1]
            new_file_name = str(("%0" + str(file_name_length) + "d") % start_count) + "." + file_type
            tool.copy_files(os.path.join(source_path, file_name), os.path.join(destination_path, new_file_name))
        # 删除临时文件夹
        tool.remove_dir(source_path)