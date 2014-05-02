# -*- coding:GBK  -*-
'''
Created on 2013-6-15

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

from common import common
import copy
import os
import time

class downloadVideo(common.Tool):

    def trace(self, msg):
        super(downloadVideo, self).trace(msg, self.isShowError, self.traceLogPath)
    
    def printErrorMsg(self, msg):
        super(downloadVideo, self).printErrorMsg(msg, self.isShowError, self.errorLogPath)
        
    def printStepMsg(self, msg):
        super(downloadVideo, self).printStepMsg(msg, self.isShowError, self.stepLogPath)
        
    def __init__(self):
        processPath = os.getcwd()
        configFile = open(processPath + "\\..\\common\\config.ini", "r")
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
        # ��������
        self.isLog = self.getConfig(config, "IS_LOG", 1, 2)
        self.isShowError = self.getConfig(config, "IS_SHOW_ERROR", 1, 2)
        self.isDebug = self.getConfig(config, "IS_DEBUG", 1, 2)
        self.isShowStep = self.getConfig(config, "IS_SHOW_STEP", 1, 2)
        # ����
        self.isProxy = self.getConfig(config, "IS_PROXY", 2, 2)
        self.proxyIp = self.getConfig(config, "PROXY_IP", "127.0.0.1", 0)
        self.proxyPort = self.getConfig(config, "PROXY_PORT", "8087", 0)
        # �ļ�·��
        self.errorLogPath = self.getConfig(config, "ERROR_LOG_FILE_NAME", "\\log\\errorLog.txt", 3)
        if self.isLog == 0:
            self.traceLogPath = ""
            self.stepLogPath = ""
        else:
            self.traceLogPath = self.getConfig(config, "TRACE_LOG_FILE_NAME", "\\log\\traceLog.txt", 3)
            self.stepLogPath = self.getConfig(config, "STEP_LOG_FILE_NAME", "\\log\\stepLog.txt", 3)
        self.userIdListFilePath = self.getConfig(config, "USER_ID_LIST_FILE_NAME", "\\info\\idlist.txt", 3)
        self.resultFilePath = self.getConfig(config, "GET_VIDEO_DOWNLOAD_URL_FILE_NAME", "\\info\\get_result.html", 3)
        self.printMsg("�����ļ���ȡ���")
        
    def main(self):
        startTime = time.time()
        # �жϸ���Ŀ¼�Ƿ����
        # ��־�ļ�����Ŀ¼
        if self.isLog == 1:
            stepLogDir = os.path.dirname(self.stepLogPath)
            if not self.createDir(stepLogDir):
                self.printErrorMsg("����������־Ŀ¼��" + stepLogDir + " ʧ�ܣ����������")
                self.processExit()
            self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + stepLogDir)
            traceLogDir = os.path.dirname(self.traceLogPath)
            if not self.createDir(traceLogDir):
                self.printErrorMsg("����������־Ŀ¼��" + traceLogDir + " ʧ�ܣ����������")
                self.processExit()
            self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + traceLogDir)
        errorLogDir = os.path.dirname(self.errorLogPath)
        if not self.createDir(errorLogDir):
            self.printErrorMsg("����������־Ŀ¼��" + errorLogDir + " ʧ�ܣ����������")
            self.processExit()
        self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + errorLogDir)
        # ��ƵURL�����ļ�
        videoUrlFileDir = os.path.dirname(self.resultFilePath)
        if not self.createDir(videoUrlFileDir):
            self.printStepMsg("��Ƶ���ص�ַҳ��Ŀ¼�������ļ��У�" + traceLogDir)
            self.processExit()
        self.printStepMsg("��Ƶ���ص�ַҳ��Ŀ¼�����ڣ������ļ��У�" + videoUrlFileDir)
        # ��Ƶurl�����html�ļ�
        if os.path.exists(self.resultFilePath):
            isDelete = False
            while not isDelete:
                # �ֶ������Ƿ�ɾ���ɴ浵�ļ�
                input = raw_input(self.getTime() + " ��Ƶ���ص�ַҳ�棺" + self.resultFilePath + " �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ�����������? (Y)es or (N)o��")
                try:
                    input = input.lower()
                    if input in ["y", "yes"]:
                        isDelete = True
                    elif input in ["n", "no"]:
                        self.processExit()
                except Exception, e:
                    self.printErrorMsg(str(e))
                    pass
                resultFile = open(self.resultFilePath, "w")
                resultFile.close()
        # ���ô���
        if self.isProxy == 1 or self.isProxy == 2:
            self.proxy(self.proxyIp, self.proxyPort, "https")
        # Ѱ��idlist�����û�н�������
        userIdList = {}
        if os.path.exists(self.userIdListFilePath):
            userListFile = open(self.userIdListFilePath, "r")
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
            self.printErrorMsg("�û�ID�浵�ļ�: " + self.userIdListFilePath + "�����ڣ����������")
            self.processExit()
        newUserIdListFilePath = os.getcwd() + "\\info\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(self.userIdListFilePath)[-1]
        newUserIdListFile = open(newUserIdListFilePath, "w")
        newUserIdListFile.close()
        # ���ƴ���浵�ļ�
        newUserIdList = copy.deepcopy(userIdList)
        for newUserId in newUserIdList:
            # ���û�����֣���������uid����
            if len(newUserIdList[newUserId]) < 2:
                newUserIdList[newUserId].append(newUserIdList[newUserId][0])
            # image count
            if len(newUserIdList[newUserId]) < 3:
                newUserIdList[newUserId].append("0")
            # image URL
            if len(newUserIdList[newUserId]) < 4:
                newUserIdList[newUserId].append("")
            # video count
            if len(newUserIdList[newUserId]) < 5:
                newUserIdList[newUserId].append("0")
            # video token
            if len(newUserIdList[newUserId]) < 6:
                newUserIdList[newUserId].append("")
            else:
                newUserIdList[newUserId][5] = ""
            # �����Ա������Ϣ
            if len(newUserIdList[newUserId]) < 7:
                newUserIdList[newUserId].append("")
                
        allVideoCount = 0
        # ѭ����ȡÿ��id
        for userId in userIdList:
            userName = newUserIdList[userId][1]
            self.printStepMsg("ID: " + str(userId) + ", ����: " + userName)
            # ��ʼ������
            videoCount = 0
            videoUrlList = []
            # ����д浵��¼����ֱ���ҵ���ǰһ��һ�µĵ�ַ�����������쳣
            if len(userIdList[userId]) >= 6 and userIdList[userId][2] != '':
                isError = True
            else:
                isError = False
            videoAlbumUrl = "https://plus.google.com/" + userId + "/videos"
            self.trace("��Ƶר����ַ��" + videoAlbumUrl)
            videoAlbumPage = self.doGet(videoAlbumUrl)
            if videoAlbumPage:
                videoUrlIndex = videoAlbumPage.find("&quot;https://video.googleusercontent.com/?token")
                while videoUrlIndex != -1:
                    videoUrlStart = videoAlbumPage.find("http", videoUrlIndex)
                    videoUrlStop = videoAlbumPage.find("&quot;", videoUrlStart)
                    videoUrl = videoAlbumPage[videoUrlStart:videoUrlStop].replace("\u003d", "=")
                    # video token ȡǰ20λ
                    tokenStart = videoUrl.find("?token=") + 7
                    videoToken = videoUrl[tokenStart:tokenStart + 20]
                    # ����һ����Ƶ��token���浽��id list��
                    if newUserIdList[userId][5] == "":
                        newUserIdList[userId][5] = videoToken
                    # �ҵ��ϴα������Ƶ
                    if len(userIdList[userId]) >= 6:
                        if videoToken == userIdList[userId][5]:
                            isError = False
                            break
                    # �ж��Ƿ��ظ�
                    if videoUrl in videoUrlList:
                        videoUrlIndex = videoAlbumPage.find("&quot;https://video.googleusercontent.com/?token", videoUrlIndex + 1)
                        continue
                    videoUrlList.append(videoUrl)
                    videoCount += 1
                    videoUrlIndex = videoAlbumPage.find("&quot;https://video.googleusercontent.com/?token", videoUrlIndex + 1)
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
                newUserIdList[userId][4] = str(int(newUserIdList[userId][4]) + videoCount)
                resultFile = open(self.resultFilePath, "a")
                while videoUrlList != []:
                    videoUrl = videoUrlList.pop()
                    index += 1
                    resultFile.writelines("<a href=" + videoUrl + ">" + str(userName + "_" + "%03d" % index) + "</a><br>\n")
                resultFile.close()
                
            if isError:
                if newUserIdList[userId][5] == "":
                    if len(userIdList[userId]) >= 6 and userIdList[userId][5] != "":
                        newUserIdList[userId][5] = userIdList[userId][5]
                else:
                    self.printErrorMsg(userName + "��Ƶ�����쳣�����ֶ����")
                    
            # ����������Ϣ
            newUserIdListFile = open(newUserIdListFilePath, "a")
            newUserIdListFile.write("\t".join(newUserIdList[userId]) + "\n")
            newUserIdListFile.close()
        
        # ���򲢱����µ�idList.txt
        tmpList = []
        tmpUserIdList = sorted(newUserIdList.keys())
        for index in tmpUserIdList:
            tmpList.append("\t".join(newUserIdList[index]))
        newUserIdListString = "\n".join(tmpList)
        newUserIdListFilePath = os.getcwd() + "\\info\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(self.userIdListFilePath)[-1]
        self.printStepMsg("�����´浵�ļ���" + newUserIdListFilePath)
        newUserIdListFile = open(newUserIdListFilePath, "w")
        newUserIdListFile.write(newUserIdListString)
        newUserIdListFile.close()
        
        stopTime = time.time()
        self.printStepMsg("�浵�ļ��������û���Ƶ��ַ�ѳɹ���ȡ����ʱ" + str(int(stopTime - startTime)) + "�룬������Ƶ��ַ" + str(allVideoCount) + "��")
        
if __name__ == "__main__":
    downloadVideo().main()