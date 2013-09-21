# -*- coding:GBK  -*-
'''
Created on 2013-6-23

@author: rena
'''

from common import common
import codecs
import os

class getMemberList(common.Tool):
        
    def __init__(self):
        # ��ȡ�����ļ�
        processPath = os.getcwd()
        configFile = open(processPath + "\\config.ini", 'r')
        lines = configFile.readlines()
        configFile.close()
        config = {}
        for line in lines:
            line = line.lstrip().rstrip().replace(" ", "")
            if len(line) > 1 and line[0] != "#":
                try:
                    line = line.split("=")
                    config[line[0]] = line[1]
                except Exception, e:
                    self.printMsg(str(e))
                    pass
        # �����ļ���ȡ������Ϣ
        # ��̳���
        self.fid = self.getConfig(config, "FID", 1, 2)
        self.tid = self.getConfig(config, "TID", 1, 2)
        self.endPageCount = self.getConfig(config, "END_PAGE_COUNT", 1, 2)
        self.startPageCount = self.getConfig(config, "START_PAGE_COUNT", 1, 2)
        # ����ϵͳ&�����
        self.browerVersion = self.getConfig(config, "BROWSER_VERSION", 2, 2)
        self.osVersion = self.getConfig(config, "OS_VERSION", 1, 2)
        # cookie
        self.isAutoGetCookie = self.getConfig(config, "IS_AUTO_GET_COOKIE", 1, 2)
        if self.isAutoGetCookie == 0:
            self.cookiePath = self.getConfig(config, "COOKIE_PATH", "", 0)
        else:
            self.cookiePath = self.getDefaultBrowserCookiePath(self.osVersion, self.browerVersion)
        self.printMsg("config init succeed")
        
    def main(self):
        # ����ϵͳcookies
        if not self.cookie(self.cookiePath, self.browerVersion):
            self.printMsg("���������cookiesʧ�ܣ����������")
            self.processExit() 
        url = "http://club.snh48.com/forum.php?mod=viewthread&tid=%s&extra=&page=%s"  # ���ӵ�ַ
        self.ipUrl = "http://club.snh48.com/forum.php?mod=topicadmin&action=getip&fid=%s&tid=%s&pid=%s"  # ip��ѯ��ַ
        floor = 1
        pageCount = self.startPageCount
        uidList = []
        ipList = []
        ipList2 = []
        isCorrectFlag = "�ܸ���"
        isIncorrectFlag = "����"
        resultFile = codecs.open(str(self.tid) + ".txt", 'w', 'utf-8')
        resultFile.write("¥��\tuid\t�û���\t�Ƿ���ȷ\tip\t�Ƿ�ʵ��\t������ע\n")
        page = self.doGet(url % (self.tid, self.startPageCount))
        while page:
            page= page.decode('utf-8')
            index = page.find('<div class="authi"><a href="home.php?mod=space&amp;uid=')
            while index != -1:
                # ¥��
                if floor == 1:
                    floorName = "¥��"
                elif floor == 2:
                    floorName = "ɳ��"
                elif floor == 3:
                    floorName = "���"
                elif floor == 4:
                    floorName = "�ذ�"
                else:
                    floorName = str(floor)
                    
                # uid
                uid = page[index + 55:page.find('"', index + 55)]
                
                # ��Ա��
                name = page[page.find('>', index + 55) + 1:page.find('</a>', index)]
                # �����Ƿ���ȷ
                scoreIndex = page.find('<tbody class="ratl_l">', index, page.find('">����</a>', index))
                score = ""
                if scoreIndex != -1:
                    scoreStart = page.find('<td class="xg1">', scoreIndex)
                    scoreStop = page.find('</tbody>', scoreIndex)
                    while scoreStart != -1:
                        score += page[scoreStart + 16:page.find('</td>', scoreStart)]
                        scoreStart = page.find('<td class="xg1">', scoreStart + 1, scoreStop)
                result = ""
                if score.find(isCorrectFlag) != -1:
                    result = "Y"
                elif  score.find(isIncorrectFlag) != -1:
                    result = "N"
                else:
                    result = score
        
                # ����Ƿ��ж��α༭
                remarks = ""
                if page.find('<i class="pstatus">', index, page.find('<input type="checkbox" id="', index)) != -1:
                    remarks = "���α༭"
                    result = "N"
                
                # ���ʵ����֤
                isReallyName = ""
                if page.find("ʵ����֤", index, page.find('</div>', index)) == -1:
                    isReallyName = "δʵ����֤"
                    result = ""
                
                # ip
                if floor == 1:
                    ip = ""
                    ip2 = ""
                else:
                    pidStart = page.find('<div id="userinfo', index) 
                    pid = page[pidStart + len('<div id="userinfo'):page.find('_', pidStart)]
                    ipPage = self.doGet(self.ipUrl % (self.fid, self.tid, pid))
                    ip = ipPage[ipPage.find("<b>") + 3:ipPage.find("</b>")]
                    ip2 = ".".join(ip.split(".")[:2])
                # ����Ƿ���λش�
                if uid in uidList:
                    answerCount = uidList.count(uid)
                    lastFloor = 0
                    for i in range(answerCount):
                        lastFloor = uidList.index(uid, lastFloor + 1)
                    remarks += "��λش���һ�λش�¥��" + str(lastFloor + 1)                       
                uidList.append(uid)
                
                # ���ip�Ƿ����ظ�
                if ip in ipList:
                    if remarks == "":
                        remarks += " ip��" + str(ipList.index(ip) + 1) + "¥��ͬ"
                elif ip2 in ipList2:
                    remarks = " ip��" + str(ipList.index(ip) + 1) + "¥����"
                ipList.append(ip)
                ipList2.append(ip)
                resultFile.write(floorName + "\t" + uid + "\t" + name + "\t" + result + "\t" + ip + "\t" + isReallyName + "\t" + remarks + "\n")
                index = page.find('<div class="authi"><a href="home.php?mod=space&amp;uid=', index + 1)
                floor += 1
            pageCount += 1
            # ���ӽ������˳�
            if pageCount > self.endPageCount:
                break
            page = self.doGet(url % (self.tid, pageCount))
            
        self.printMsg("ͳ�ƽ���")
          
if __name__ == '__main__':
    getMemberList().main()
