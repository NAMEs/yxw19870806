# -*- coding:GBK  -*-
'''
Created on 2013-6-15

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

import copy
import os
import time
import sys
import traceback
import urllib2

class downloadVideo():
    
    def doGet(self, url):
    # http����
        global IS_SET_TIMEOUT
        if url.find("http") == -1:
            return None
        count = 0
        while 1:
            try:
                request = urllib2.Request(url)
                # ����ͷ��Ϣ
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 FirePHP/0.7.2')
                # ���÷��ʳ�ʱ
                if sys.version_info < (2, 7):
                    if not IS_SET_TIMEOUT:
                        urllib2.socket.setdefaulttimeout(20)
                        IS_SET_TIMEOUT = True
                    response = urllib2.urlopen(request)
                else:
                    response = urllib2.urlopen(request, timeout=20)
                return response.read()
            except Exception, e:
                # �����޷�����
                if str(e).find("[Errno 10061] ") != -1:
                    input = raw_input("�޷����ʴ��������������������á��Ƿ���Ҫ��������(Y)es or (N)o��").lower()
                    if input in ["y", "yes"]:
                        pass
                    elif input in ["n", "no"]:
                        sys.exit()
                # ��ʱ
                elif str(e).find("timed out") != -1:
                    self.printMsg("����ҳ�泬ʱ�������������Ժ�")
                else:
                    self.printMsg(str(e))
                    traceback.print_exc()
            count += 1
            if count > 10:
                self.printMsg("�޷�����ҳ�棺" + url)
                return False
    
    def proxy(self, ip, port):
    # ���ô���
        proxyHandler = urllib2.ProxyHandler({'https':"http://" + ip + ":" + port})
        opener = urllib2.build_opener(proxyHandler)
        urllib2.install_opener(opener)
        self.printMsg("���ô���ɹ�")
                
    def getConfig(self, config, key, defaultValue, mode, prefix=None, postfix=None):
    # ��ȡ�����ļ�
    # config : �ֵ��ʽ���磺{key1:value1, key2:value2}
    # mode 0 : ֱ�Ӹ�ֵ
    # mode 1 : �ַ���ƴ��
    # mode 2 : ȡ��
    # mode 3 : �ļ�·������'\'��ͷ��Ϊ��ǰĿ¼�´���
    # prefix: ǰ׺��ֻ����mode=1ʱ��Ч
    # postfix: ��׺��ֻ����mode=1ʱ��Ч
        value = None
        if config.has_key(key):
            if mode == 0:
                value = config[key]
            elif mode == 1:
                value = config[key]
                if prefix != None:
                    value = prefix + value
                if postfix != None:
                    value = value + postfix
            elif mode == 2:
                try:
                    value = int(config[key])
                except:
                    self.printMsg("�����ļ�config.ini��keyΪ'" + key + "'��ֵ������һ��������ʹ�ó���Ĭ������")
                    traceback.print_exc()
                    value = defaultValue
            elif mode == 3:
                value = config[key]
                if value[0] == "\\":
                    value = os.getcwd() + value
                return value
        else:
            self.printMsg("�����ļ�config.ini��û���ҵ�keyΪ'" + key + "'�Ĳ�����ʹ�ó���Ĭ������")
            value = defaultValue
        return value
    
    def printMsg(self, msg, isTime=True):
        if isTime:
            msg = self.getTime() + " " + msg
        print msg
    
    def getTime(self):
        return time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    
    def writeFile(self, msg, filePath):
        logFile = open(filePath, 'a')
        logFile.write(msg + "\n")
        logFile.close()
    
    def createDir(self, path):
        count = 0
        while 1:
            try:
                if count >= 5:
                    return False
                os.makedirs(path)
                if os.path.isdir(path):
                    return True
            except Exception, e:
                self.printMsg(str(e))
                time.sleep(5)
                traceback.print_exc()
            count +=1
        
    def removeDirFiles(self, dirPath): 
        for fileName in os.listdir(dirPath): 
            targetFile = os.path.join(dirPath, fileName) 
            if os.path.isfile(targetFile): 
                os.remove(targetFile)
                
    def processExit(self):
        sys.exit()
    
    def trace(self, msg):
        if self.isDebug == 1:
            msg = self.getTime() + " " + msg
    #        self.printMsg(msg, False)
            if self.isLog == 1:
                self.writeFile(msg, self.traceLogPath)
    
    def printErrorMsg(self, msg):
        if self.isShowError == 1:
            msg = self.getTime() + " [Error] " + msg
            self.printMsg(msg, False)
            if self.isLog == 1:
                if msg.find("HTTP Error 500") != -1:
                    return
                if msg.find("urlopen error The read operation timed out") != -1:
                    return
                self.writeFile(msg, self.errorLogPath)
    
    def printStepMsg(self, msg):
        if self.isShowStep == 1:
            msg = self.getTime() + " " + msg
            self.printMsg(msg, False)
            if self.isLog == 1:
                self.writeFile(msg, self.stepLogPath)
    
    def __init__(self):
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
        # �����ļ���ȡ��־�ļ�·��
        self.errorLogPath = self.getConfig(config, "ERROR_LOG_FILE_NAME", "\\log\\errorLog.txt", 3)
        self.traceLogPath = self.getConfig(config, "TRACE_LOG_FILE_NAME", "\\log\\traceLog.txt", 3)
        self.stepLogPath = self.getConfig(config, "STEP_LOG_FILE_NAME", "\\log\\stepLog.txt", 3)
        self.memberUIdListFilePath = self.getConfig(config, "USER_ID_LIST_FILE_NAME", "\\info\\idlist.txt", 3)
        self.resultFilePath = self.getConfig(config, "GET_VIDEO_DOWNLOAD_URL_FILE_NAME", "\\info\\get_result.html", 3)
        # �����ļ���ȡ��������
        self.isLog = self.getConfig(config, "IS_LOG", 1, 2)
        self.isShowError = self.getConfig(config, "IS_SHOW_ERROR", 1, 2)
        self.isDebug = self.getConfig(config, "IS_DEBUG", 1, 2)
        self.isShowStep = self.getConfig(config, "IS_SHOW_STEP", 1, 2)
        self.isProxy = self.getConfig(config, "IS_PROXY", 2, 2)
        self.proxyIp = self.getConfig(config, "PROXY_IP", "127.0.0.1", 0)
        self.proxyPort = self.getConfig(config, "PROXY_PORT", "8087", 0)
        self.printMsg("�����ļ���ȡ���")
        
    def main(self):
        startTime = time.time()
        # �жϸ���Ŀ¼�Ƿ����
        # ��־�ļ�����Ŀ¼
        if self.isLog == 1:
            stepLogDir = os.path.dirname(self.stepLogPath)
            if not os.path.exists(stepLogDir):
                if not self.createDir(stepLogDir):
                    self.printErrorMsg("����������־Ŀ¼��" + stepLogDir + " ʧ�ܣ����������")
                    self.processExit()
                self.printStepMsg("������־Ŀ¼�����ڣ������ļ���: " + stepLogDir)
            errorLogDir = os.path.dirname(self.errorLogPath)
            if not os.path.exists(errorLogDir):
                if not self.createDir(errorLogDir):
                    self.printErrorMsg("����������־Ŀ¼��" + errorLogDir + " ʧ�ܣ����������")
                    self.processExit()
                self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + errorLogDir)
            traceLogDir = os.path.dirname(self.traceLogPath)
            if not os.path.exists(traceLogDir):
                if not self.createDir(traceLogDir):
                    self.printErrorMsg("����������־Ŀ¼��" + traceLogDir + " ʧ�ܣ����������")
                    self.processExit()
                self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + traceLogDir)
        videoUrlFileDir = os.path.dirname(self.resultFilePath)
        if not os.path.exists(videoUrlFileDir):
            if not self.createDir(videoUrlFileDir):
                self.printStepMsg("��Ƶ���ص�ַҳ��Ŀ¼�������ļ��У�" + traceLogDir)
                self.processExit()
            self.printStepMsg("��Ƶ���ص�ַҳ��Ŀ¼�����ڣ������ļ��У�" + videoUrlFileDir)
        # ��Ƶurl�����html�ļ�
        if os.path.exists(self.resultFilePath):
            isDelete = False
            while not isDelete:
                # �ֶ������Ƿ�ɾ���ɴ浵�ļ�
                input = raw_input("��Ƶ���ص�ַҳ�棺" + self.resultFilePath + " �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ�����������? (Y)es or (N)o��")
                try:
                    input = input.lower()
                    if input in ["y", "yes"]:
                        isDelete = True
                    elif input in ["n", "no"]:
                        self.processExit()
                except:
                    pass
                resultFile = open(self.resultFilePath, 'w')
                resultFile.close()
        # ���ô���
        if self.isProxy == 1 or self.isProxy == 2:
            self.proxy(self.proxyIp, self.proxyPort)
        # Ѱ��idlist�����û�н�������
        userIdList = {}
        if os.path.exists(self.memberUIdListFilePath):
            userListFile = open(self.memberUIdListFilePath, 'r')
            allUserList = userListFile.readlines()
            userListFile.close()
            for userInfo in allUserList:
                if len(userInfo) < 10:
                    continue
                userInfo = userInfo.replace(" ", "")
                userInfo = userInfo.replace("\n", "")
                userInfoList = userInfo.split("\t")
                userIdList[userInfoList[0]] = userInfoList
        else:
            self.printErrorMsg("�û�ID�浵�ļ�: " + self.memberUIdListFilePath + "�����ڣ����������")
            self.processExit()
        newMemberUidListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.memberUIdListFilePath)[-1]
        newMemberUidListFile = open(newMemberUidListFilePath, 'w')
        newMemberUidListFile.close()
        # ���ƴ���浵�ļ�
        newMemberUidList = copy.deepcopy(userIdList)
        for newUserId in newMemberUidList:
            # ���û�����֣���������uid����
            if len(newMemberUidList[newUserId]) < 2:
                newMemberUidList[newUserId].append(newMemberUidList[newUserId][0])
            # image count
            if len(newMemberUidList[newUserId]) < 3:
                newMemberUidList[newUserId].append("0")
            # image URL
            if len(newMemberUidList[newUserId]) < 4:
                newMemberUidList[newUserId].append("")
            # video count
            if len(newMemberUidList[newUserId]) < 5:
                newMemberUidList[newUserId].append("0")
            # video token
            if len(newMemberUidList[newUserId]) < 6:
                newMemberUidList[newUserId].append("")
            else:
                newMemberUidList[newUserId][5] = ""
            # ����member ������Ϣ
            if len(newMemberUidList[newUserId]) < 7:
                newMemberUidList[newUserId].append("")
                
        allVideoCount = 0
        # ѭ����ȡÿ��id
        for userId in userIdList:
            userName = newMemberUidList[userId][1]
            self.printStepMsg("UID: " + str(userId) + ", ����: " + userName)
            # ��ʼ������
            videoCount = 0
            videoUrlList = []
            videoAlbumUrl = 'https://plus.google.com/' + userId + '/videos'
            self.trace("��Ƶר����ַ��" + videoAlbumUrl)
            videoAlbumPage = self.doGet(videoAlbumUrl)
            if videoAlbumPage:
                videoUrlIndex = videoAlbumPage.find('&quot;https://video.googleusercontent.com/?token')
                while videoUrlIndex != -1:
                    videoUrlStart = videoAlbumPage.find("http", videoUrlIndex)
                    videoUrlStop = videoAlbumPage.find('&quot;', videoUrlStart)
                    videoUrl = videoAlbumPage[videoUrlStart:videoUrlStop].replace("\u003d", "=")
                    # video token ȡǰ20λ
                    tokenStart = videoUrl.find("?token=") + 7
                    videoToken = videoUrl[tokenStart:tokenStart + 20]
                    # ����һ����Ƶ��token���浽��id list��
                    if newMemberUidList[userId][5] == "":
                        newMemberUidList[userId][5] = videoToken
                    if len(userIdList[userId]) >= 6:
                        if videoToken == userIdList[userId][5]:
                            break
                    # �ж��Ƿ��ظ�
                    if videoUrl in videoUrlList:
                        videoUrlIndex = videoAlbumPage.find('&quot;https://video.googleusercontent.com/?token', videoUrlIndex + 1)
                        continue
                    videoUrlList.append(videoUrl)
                    videoCount += 1
                    videoUrlIndex = videoAlbumPage.find('&quot;https://video.googleusercontent.com/?token', videoUrlIndex + 1)
            else:
                self.printErrorMsg("�޷���ȡ��Ƶ��ҳ: " + videoAlbumUrl)
            # ����������Ƶurl���ļ�
            if videoCount > 0:
                allVideoCount += videoCount
                index = 0
                try:
                    index = int(userIdList[userId][4])
                except:
                    pass
                newMemberUidList[userId][4] = str(int(newMemberUidList[userId][4]) + videoCount)
                resultFile = open(self.resultFilePath, 'a')
                while videoUrlList != []:
                    videoUrl = videoUrlList.pop()
                    index += 1
                    resultFile.writelines("<a href=" + videoUrl + ">" + str(userName + "_" + "%03d" % index) + "</a><br>\n")
                resultFile.close()
            # ����������Ϣ
            newMemberUidListFile = open(newMemberUidListFilePath, 'a')
            newMemberUidListFile.write("\t".join(newMemberUidList[userId]) + "\n")
            newMemberUidListFile.close()

        # ���򲢱����µ�idList.txt
        tmpList = []
        tmpUserIdList = sorted(newMemberUidList.keys())
        for index in tmpUserIdList:
            tmpList.append("\t".join(newMemberUidList[index]))
        newMemberUidListString = "\n".join(tmpList)
        newMemberUidListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.memberUIdListFilePath)[-1]
        self.printStepMsg("�����´浵�ļ�: " + newMemberUidListFilePath)
        newMemberUidListFile = open(newMemberUidListFilePath, 'w')
        newMemberUidListFile.write(newMemberUidListString)
        newMemberUidListFile.close()
        
        stopTime = time.time()
        self.printStepMsg("�浵�ļ��������û���Ƶ��ַ�ѳɹ���ȡ����ʱ" + str(int(stopTime - startTime)) + "�룬������Ƶ��ַ" + str(allVideoCount) + "��")
        
if __name__ == '__main__':
    downloadVideo().main()
