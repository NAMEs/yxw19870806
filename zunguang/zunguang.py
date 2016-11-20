# -*- coding:UTF-8  -*-
"""
美图赚赚图片爬虫
http://meituzz.com/
@author: hikaru
email: hikaru870806@hotmail.com
如有问题或建议请联系
"""
from common import log, robot, tool
import json
import os
import re


# 根据页面内容获取图片地址列表
def get_one_page_album_data(page_count):
    album_url = "http://www.zunguang.com/index.php?c=api&yc=blog&ym=getOneBlog"
    post_data = {"bid": page_count}
    album_return_code, album_data = tool.http_request(album_url, post_data)[:2]
    if album_return_code == 1:
        try:
            album_data = json.loads(album_data)
        except ValueError:
            return None
        if robot.check_sub_key(("body",), album_data) and robot.check_sub_key(("blog",), album_data["body"]):
            album_body = album_data["body"]["blog"][0]
            if robot.check_sub_key(("title", "attr"), album_body) and robot.check_sub_key(("img",), album_body["attr"]):
                return album_body
    return None


class ZunGuang(robot.Robot):
    def __init__(self):
        sys_config = {
            robot.SYS_DOWNLOAD_IMAGE: True,
            robot.SYS_NOT_CHECK_SAVE_DATA: True,
        }
        robot.Robot.__init__(self, sys_config)

        tool.print_msg("配置文件读取完成")

    def main(self):
        # 解析存档文件，获取上一次的album id
        page_count = 1
        if os.path.exists(self.save_data_path):
            save_file = open(self.save_data_path, "r")
            save_info = save_file.read()
            save_file.close()
            page_count = int(save_info.strip())

        total_image_count = 0
        error_count = 0
        is_over = False
        while not is_over:
            album_data = get_one_page_album_data(page_count)

            if album_data is None:
                log.error("第%s页相册访问失败" % page_count)
                break

            # 下载目录标题

            title = str(album_data["title"].encode("utf-8"))
            for filter_char in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]:
                title = title.replace(filter_char, " ")  # 过滤一些windows文件名屏蔽的字符
            title = title.strip().rstrip(".")  # 去除前后空格以及后缀的
            if title:
                image_path = os.path.join(self.image_download_path, "%04d %s" % (page_count, title))
            else:
                image_path = os.path.join(self.image_download_path, page_count)
            if not tool.make_dir(image_path, 0):
                # 目录出错，把title去掉后再试一次，如果还不行退出
                log.error("第%s页创建相册目录 %s 失败，尝试不使用title" % (page_count, image_path))
                post_path = os.path.join(image_path, page_count)
                if not tool.make_dir(post_path, 0):
                    log.error("第%s页创建相册目录 %s 失败" % (page_count, image_path))
                    tool.process_exit()

            image_count = 1
            for image_data in album_data["attr"]["img"]:
                image_url = "http://www.zunguang.com/%s" % str(image_data["url"])
                log.step("开始下载第%s页第%s张图片 %s" % (page_count, image_count, image_url))

                file_type = image_url.split(".")[-1]
                file_path = os.path.join(image_path, "%03d.%s" % (image_count, file_type))
                try:
                    if tool.save_net_file(image_url, file_path, True):
                        log.step("第%s页第%s张图片下载成功" % (page_count, image_count))
                        image_count += 1
                    else:
                        log.error("第%s页第%s张图片 %s 下载失败" % (page_count, image_count, image_url))
                except SystemExit:
                    log.step("提前退出")
                    tool.remove_dir(image_path)
                    is_over = True
                    break

            if not is_over:
                total_image_count += image_count - 1
                page_count += 1

        # 重新保存存档文件
        save_data_dir = os.path.dirname(self.save_data_path)
        if not os.path.exists(save_data_dir):
            tool.make_dir(save_data_dir, 0)
        save_file = open(self.save_data_path, "w")
        save_file.write(str(page_count))
        save_file.close()

        log.step("全部下载完毕，耗时%s秒，共计图片%s张" % (self.get_run_time(), total_image_count))


if __name__ == "__main__":
    ZunGuang().main()
