# -*- coding:GBK  -*-
'''
Created on 2013-4-8

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

from common import common
import copy
import os
import shutil
import time

class downloadImage(common.Tool):
    
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
        configFile = open(processPath + "\\..\\common\\config.ini", 'r')
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
        self.imageDownloadPath = self.getConfig(config, "IMAGE_DOWNLOAD_DIR_NAME", "\\photo", 3)
        self.imageTempPath = self.getConfig(config, "IMAGE_TEMP_DIR_NAME", "\\tempImage", 3)
        self.memberUIdListFilePath = self.getConfig(config, "MEMBER_UID_LIST_FILE_NAME", "\\info\\idlist.txt", 3)
        # �����ļ���ȡ��������
        self.isLog = self.getConfig(config, "IS_LOG", 1, 2)
        self.isShowError = self.getConfig(config, "IS_SHOW_ERROR", 1, 2)
        self.isDebug = self.getConfig(config, "IS_DEBUG", 1, 2)
        self.isShowStep = self.getConfig(config, "IS_SHOW_STEP", 1, 2)
        self.isSort = self.getConfig(config, "IS_SORT", 1, 2)
        self.getImageCount = self.getConfig(config, "GET_IMAGE_COUNT", 1, 2)
        self.isProxy = self.getConfig(config, "IS_PROXY", 2, 2)
        self.proxyIp = self.getConfig(config, "PROXY_IP", "127.0.0.1", 0)
        self.proxyPort = self.getConfig(config, "PROXY_PORT", "8087", 0)
        self.printMsg("config init succeed")

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
                self.printStepMsg("������־Ŀ¼�����ڣ������ļ���: " + errorLogDir)
            traceLogDir = os.path.dirname(self.traceLogPath)
            if not os.path.exists(traceLogDir):
                if not self.createDir(traceLogDir):
                    self.printErrorMsg("����������־Ŀ¼��" + traceLogDir + " ʧ�ܣ����������")
                    self.processExit()
                self.printStepMsg("������־Ŀ¼�����ڣ������ļ���: " + traceLogDir)
        # ͼƬ����Ŀ¼
        if os.path.exists(self.imageDownloadPath):
            if os.path.isdir(self.imageDownloadPath):
                isDelete = False
                while not isDelete:
                    # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                    input = raw_input("ͼƬ����Ŀ¼��" + self.imageDownloadPath + " �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ��в���������(Y)es or (N)o: ")
                    try:
                        input = input.lower()
                        if input in ["y", "yes"]:
                            isDelete = True
                        elif input in ["n", "no"]:
                            self.processExit()
                    except:
                        pass
                self.printStepMsg("ɾ��ͼƬ����Ŀ¼: " + self.imageDownloadPath)
                # ɾ��Ŀ¼
                shutil.rmtree(self.imageDownloadPath, True)
                # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                while os.path.exists(self.imageDownloadPath):
                    time.sleep(5)
            else:
                self.printStepMsg("ͼƬ����Ŀ¼: " + self.imageDownloadPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
                os.remove(self.imageDownloadPath)
        self.printStepMsg("����ͼƬ����Ŀ¼: " + self.imageDownloadPath)
        if not self.createDir(self.imageDownloadPath):
            self.printErrorMsg("����ͼƬ����Ŀ¼��" + self.imageDownloadPath + " ʧ�ܣ����������")
            self.processExit()
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
        # ������ʱ�浵�ļ�
        newMemberUidListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.memberUIdListFilePath)[-1]
        newMemberUidListFile = open(newMemberUidListFilePath, 'w')
        newMemberUidListFile.close()
        # ���ƴ���浵�ļ�
        newMemberUidList = copy.deepcopy(userIdList)
        for newUserId in newMemberUidList:
            # ���û�����֣���������uid����
            if len(newMemberUidList[newUserId]) < 2:
                newMemberUidList[newUserId].append(newMemberUidList[newUserId][0])
            # ���û�г���image count����Ϊ0
            if len(newMemberUidList[newUserId]) < 3:
                newMemberUidList[newUserId].append("0")
            # ������һ��image URL
            # ���ÿմ�ű��ε�һ�Ż�ȡ��image URL
            if len(newMemberUidList[newUserId]) < 4:
                newMemberUidList[newUserId].append("")
            else:
                newMemberUidList[newUserId][3] = ""
            # video count
            if len(newMemberUidList[newUserId]) < 5:
                newMemberUidList[newUserId].append("0")
            # video token
            if len(newMemberUidList[newUserId]) < 6:
                newMemberUidList[newUserId].append("")
            # ����member ������Ϣ
            if len(newMemberUidList[newUserId]) < 7:
                newMemberUidList[newUserId].append("")
        
        allImageCount = 0
        # ѭ������ÿ��id
        for userId in sorted(userIdList.keys()):
            userName = newMemberUidList[userId][1]
            self.printStepMsg("UID: " + str(userId) + ", ����: " + userName)
            # ��ʼ������
            pageCount = 0
            imageCount = 1
            messageUrlList = []
            imageUrlList = []
            isPass = False
            isError = False
            # �����Ҫ����������ʹ����ʱ�ļ��У�����ֱ�����ص�Ŀ��Ŀ¼
            if self.isSort == 1:
                imagePath = self.imageTempPath
            else:
                imagePath = self.imageDownloadPath + "\\" + userName
            if not self.createDir(imagePath):
                self.printErrorMsg("����ͼƬ����Ŀ¼�� " + imagePath + " ʧ�ܣ����������")
                self.processExit()
            # ͼƬ����  
            while 1:
                if isPass:
                    break
                # ��ȡ��Ϣ��ҳ,offset=N��ʾ�������µ�N��N+100����Ϣ���ڵ�url
                photoAlbumUrl = "https://plus.google.com/_/photos/posts/%s?offset=%s" % (userId, pageCount)
                self.trace("���ר����ַ��" + photoAlbumUrl)
                photoAlbumPage = self.doGet(photoAlbumUrl)
                if not photoAlbumPage:
                    self.printErrorMsg("�޷���ȡ�����ҳ: " + photoAlbumUrl)
                    isPass = True
                    break
            
                # �ж���Ϣ��ҳ�ֽ�����С���Ƿ�С��300�����ص����һҳ��������
                if len(photoAlbumPage) < 300:
                    break

                messageIndex = 1
                while messageIndex != 0:
                    if isPass:
                        break
                    messageIndex = photoAlbumPage.find('[["https://picasaweb.google.com/' + userId, messageIndex)
                    messageStart = photoAlbumPage.find("http", messageIndex)
                    messageStop = photoAlbumPage.find('"', messageStart)
                    messageUrl = photoAlbumPage[messageStart:messageStop]
                    if messageIndex == -1:
                        break
                    # ����һ��image��URL���浽��id list��
                    if newMemberUidList[userId][3] == "":
                        newMemberUidList[userId][3] = messageUrl
                    # ����Ƿ������ص�ǰһ�ε�ͼƬ
                    if len(userIdList[userId]) >= 4 and userIdList[userId][3].find("picasaweb.google.com/") != -1:
                        if messageUrl == userIdList[userId][3]:
                            isPass = True
                            break
                    self.trace("message URL:" + messageUrl)
                    # �ж��Ƿ��ظ�
                    if messageUrl in messageUrlList:
                        messageIndex += 1
                        continue
                    messageUrlList.append(messageUrl)
                    messagePage = self.doGet(messageUrl)
                    if not messagePage:
                        # self.printErrorMsg("can not get messagePage: " + messageUrl)
                        self.printErrorMsg("�޷���ȡ��Ϣҳ: " + messageUrl)
                        messageIndex += 1
                        continue
                    flag = messagePage.find("<div><a href=")
                    while flag != -1:
                        imageIndex = messagePage.find("<img src=", flag, flag + 200)
                        if imageIndex == -1:
                            self.printErrorMsg("��Ϣҳ��" + messageUrl + " ��û���ҵ���ǩ'<img src='")
                            break
                        imageStart = messagePage.find("http", imageIndex)
                        imageStop = messagePage.find('"', imageStart)
                        imageUrl = messagePage[imageStart:imageStop]
                        self.trace("image URL:" + imageUrl)
                        if imageUrl in imageUrlList:
                            flag = messagePage.find("<div><a href=", flag + 1)
                            continue
                        tempList = imageUrl.split("/")
                        # ʹ�����ֱ���
                        tempList[-2] = "s0"
                        imageUrl = "/".join(tempList)
                        # �ļ�����
                        fileType = imageUrl.split(".")[-1]
                        imgByte = self.doGet(imageUrl)
                        if imgByte:
                            # ����ͼƬ
                            filename = str("%04d" % imageCount)
                            imageFile = open(imagePath + "\\" + str(filename) + "." + fileType, "wb")
                            self.printStepMsg("��ʼ���ص�" + str(imageCount) + "��ͼƬ��" + imageUrl)
                            imageFile.write(imgByte)
                            imageFile.close()
                            self.printStepMsg("���سɹ�")
                            imageCount += 1
                            # �ﵽ�����ļ��е���������������
                            if self.getImageCount > 0 and imageCount > self.getImageCount:
                                isPass = True
                                break
                        else:
                            self.printErrorMsg("��ȡͼƬ��Ϣʧ�ܣ�" + str(userId) + ": " + imageUrl)
                        flag = messagePage.find("<div><a href=", flag + 1)
                    messageIndex += 1
                pageCount += 100
                
            self.printStepMsg(userName + "������ϣ��ܹ����" + str(imageCount - 1) + "��ͼƬ")
            # �������ͼƬ�Ƿ������������һ�룬����һ�μ�¼��ͼƬ���ñ�ɾ��������ԭ����������ȫ��ͼƬ��һ������
            if int(newMemberUidList[userId][2]) != 0 and (imageCount * 2) > int(newMemberUidList[userId][2]):
                isError = True
            newMemberUidList[userId][2] = str(int(newMemberUidList[userId][2]) + imageCount - 1)
            allImageCount += imageCount - 1
            
            # ����
            if self.isSort == 1:
                imageList = sorted(os.listdir(imagePath), reverse=True)
                # �ж�����Ŀ���ļ����Ƿ����
                if len(imageList) >= 1:
                    destPath = self.imageDownloadPath + "\\" + newMemberUidList[userId][6] + "\\" + userName
                    if os.path.exists(destPath):
                        if os.path.isdir(destPath):
                            self.printStepMsg("ͼƬ����Ŀ¼: " + destPath + " �Ѵ��ڣ�ɾ����")
                            self.removeDirFiles(destPath)
                        else:
                            self.printStepMsg("ͼƬ����Ŀ¼: " + destPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ����")
                            os.remove(destPath)
                    self.printStepMsg("����ͼƬ����Ŀ¼: " + destPath)
                    if not self.createDir(destPath):
                        self.printErrorMsg("����ͼƬ����Ŀ¼�� " + destPath + " ʧ�ܣ����������")
                        self.processExit()
                    # ��������
                    if len(userIdList[userId]) >= 3:
                        count = int(userIdList[userId][2]) + 1
                    else:
                        count = 1
                    for fileName in imageList:
                        fileType = fileName.split(".")[1]
                        shutil.copyfile(imagePath + "\\" + fileName, destPath + "\\" + str("%04d" % count) + "." + fileType)
                        count += 1
                    self.printStepMsg("ͼƬ������Ŀ¼�ƶ�������Ŀ¼�ɹ�")
                # ɾ����ʱ�ļ���
                shutil.rmtree(imagePath, True)

            if isError:
                self.printErrorMsg(userName + "ͼƬ�����쳣�����ֶ����")

            # ����������Ϣ
            newMemberUidListFile = open(newMemberUidListFilePath, 'a')
            newMemberUidListFile.write("\t".join(newMemberUidList[userId]) + "\n")
            newMemberUidListFile.close()

        # ���򲢱����µ�idList.txt
        tempList = []
        tempUserIdList = sorted(newMemberUidList.keys())
        for index in tempUserIdList:
            tempList.append("\t".join(newMemberUidList[index]))
        newMemberUidListString = "\n".join(tempList)
        newMemberUidListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.memberUIdListFilePath)[-1]
        self.printStepMsg("�����´浵�ļ�: " + newMemberUidListFilePath)
        newMemberUidListFile = open(newMemberUidListFilePath, 'w')
        newMemberUidListFile.write(newMemberUidListString)
        newMemberUidListFile.close()
        
        stopTime = time.time()
        self.printStepMsg("�浵�ļ��������û�ͼƬ�ѳɹ����أ���ʱ" + str(int(stopTime - startTime)) + "�룬����ͼƬ" + str(allImageCount) + "��")

if __name__ == '__main__':
    downloadImage().main()
