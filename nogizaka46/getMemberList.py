# -*- coding:UTF-8  -*-
"""
乃木坂46 OFFICIAL BLOG成员id获取
http://http://blog.nogizaka46.com/
@author: hikaru
email: hikaru870806@hotmail.com
如有问题或建议请联系
"""
from common import tool
import re


def get_member_list():
    index_url = "http://blog.nogizaka46.com/"
    index_return_code, index_page = tool.http_request(index_url)[:2]
    if index_return_code:
        member_list_find = re.findall('<div class="unit"><a href="./([^"]*)"><img src="[^>]*alt="([^"]*)" />', index_page)
        for member_info in member_list_find:
            tool.print_msg("%s\t\t\t%s" % (member_info[0], member_info[1]), False)
        if len(member_list_find) > 0:
            tool.print_msg("复制以上内容到save.data中，删除不需要的行，即可开始运行", False)
    return None

if __name__ == "__main__":
    get_member_list()
