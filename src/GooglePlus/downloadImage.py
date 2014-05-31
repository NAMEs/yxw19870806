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
        super(downloadImage, self).trace(msg, self.isShowError, self.traceLogPath)
    
    def printErrorMsg(self, msg):
        super(downloadImage, self).printErrorMsg(msg, self.isShowError, self.errorLogPath)
        
    def printStepMsg(self, msg):
        super(downloadImage, self).printStepMsg(msg, self.isShowError, self.stepLogPath)
    
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
        self.isSort = self.getConfig(config, "IS_SORT", 1, 2)
        self.getImageCount = self.getConfig(config, "GET_IMAGE_COUNT", 0, 2)
        self.getImageUrlCount = self.getConfig(config, "GET_IMAGE_URL_COUNT", 100, 2)
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
        self.imageDownloadPath = self.getConfig(config, "IMAGE_DOWNLOAD_DIR_NAME", "\\photo", 3)
        self.imageTempPath = self.getConfig(config, "IMAGE_TEMP_DIR_NAME", "\\tempImage", 3)
        self.userIdListFilePath = self.getConfig(config, "USER_ID_LIST_FILE_NAME", "\\info\\idlist.txt", 3)
        self.printMsg("�����ļ���ȡ���")

    def main(self):
        startTime = time.time()
        # �жϸ���Ŀ¼�Ƿ����
        # ��־�ļ�����Ŀ¼
        if self.isLog == 1:
            stepLogDir = os.path.dirname(self.stepLogPath)
            if not os.path.exists(stepLogDir):
                self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + stepLogDir)
                if not self.createDir(stepLogDir):
                    self.printErrorMsg("����������־Ŀ¼��" + stepLogDir + " ʧ�ܣ����������")
                    self.processExit()
            traceLogDir = os.path.dirname(self.traceLogPath)
            if not os.path.exists(traceLogDir):
                self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + traceLogDir)
                if not self.createDir(traceLogDir):
                    self.printErrorMsg("����������־Ŀ¼��" + traceLogDir + " ʧ�ܣ����������")
                    self.processExit()
        errorLogDir = os.path.dirname(self.errorLogPath)
        if not os.path.exists(errorLogDir):
            self.printStepMsg("������־Ŀ¼�����ڣ������ļ��У�" + errorLogDir)
            if not self.createDir(errorLogDir):
                self.printErrorMsg("����������־Ŀ¼��" + errorLogDir + " ʧ�ܣ����������")
                self.processExit()
        # ͼƬ����Ŀ¼
        if os.path.exists(self.imageDownloadPath):
            if os.path.isdir(self.imageDownloadPath):
                isDelete = False
                while not isDelete:
                    # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                    input = raw_input(self.getTime() + " ͼƬ����Ŀ¼��" + self.imageDownloadPath + " �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ��в���������(Y)es or (N)o: ")
                    try:
                        input = input.lower()
                        if input in ["y", "yes"]:
                            isDelete = True
                        elif input in ["n", "no"]:
                            self.processExit()
                    except Exception, e:
                        self.printErrorMsg(str(e)) 
                        pass
                self.printStepMsg("ɾ��ͼƬ����Ŀ¼��" + self.imageDownloadPath)
                # ɾ��Ŀ¼
                shutil.rmtree(self.imageDownloadPath, True)
                # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                while os.path.exists(self.imageDownloadPath):
                    shutil.rmtree(self.imageDownloadPath, True)
                    time.sleep(5)
            else:
                self.printStepMsg("ͼƬ����Ŀ¼��" + self.imageDownloadPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
                os.remove(self.imageDownloadPath)
        self.printStepMsg("����ͼƬ����Ŀ¼��" + self.imageDownloadPath)
        if not self.createDir(self.imageDownloadPath):
            self.printErrorMsg("����ͼƬ����Ŀ¼��" + self.imageDownloadPath + " ʧ�ܣ����������")
            self.processExit()
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
        # ������ʱ�浵�ļ�
        newUserIdListFilePath = os.getcwd() + "\\info\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(self.userIdListFilePath)[-1]
        newUserIdListFile = open(newUserIdListFilePath, "w")
        newUserIdListFile.close()
        # ���ƴ���浵�ļ�
        newUserIdList = copy.deepcopy(userIdList)
        for newUserId in newUserIdList:
            # ���û�����֣���������uid����
            if len(newUserIdList[newUserId]) < 2:
                newUserIdList[newUserId].append(newUserIdList[newUserId][0])
            # ���û�г���image count����Ϊ0
            if len(newUserIdList[newUserId]) < 3:
                newUserIdList[newUserId].append("0")
            # ������һ��image URL
            # ���ÿմ�ű��ε�һ�Ż�ȡ��image URL
            if len(newUserIdList[newUserId]) < 4:
                newUserIdList[newUserId].append("")
            else:
                newUserIdList[newUserId][3] = ""
            # video count
            if len(newUserIdList[newUserId]) < 5:
                newUserIdList[newUserId].append("0")
            # video token
            if len(newUserIdList[newUserId]) < 6:
                newUserIdList[newUserId].append("")
            # �����Ա������Ϣ
            if len(newUserIdList[newUserId]) < 7:
                newUserIdList[newUserId].append("")
        
        totalImageCount = 0
        # ѭ������ÿ��id
        for userId in sorted(userIdList.keys()):
            userName = newUserIdList[userId][1]
            self.printStepMsg("ID: " + str(userId) + ", ����: " + userName)
            # ��ʼ������
            imageCount = 1
            messageUrlList = []
            imageUrlList = []
            # ����д浵��¼����ֱ���ҵ���ǰһ��һ�µĵ�ַ�����������쳣
            if len(userIdList[userId]) > 3 and userIdList[userId][3].find("picasaweb.google.com/") != -1 and int(userIdList[userId][2]) != 0:
                isError = True
            else:
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
#            photoAlbumUrl = "https://plus.google.com/photos/%s/albums/posts?banner=pwa" % (userId)
            photoAlbumUrl = 'https://plus.google.com/_/photos/pc/read/'
            now = time.time() * 100
            key = ''
            postData = 'f.req=[["posts",null,null,"synthetic:posts:%s",3,"%s",null],[%s,1,null],"%s",null,null,null,null,null,null,null,2]&at=AObGSAj1ll9iGT-1d05vTuxV5yygWelh9g:%s&' % (userId, userId, self.getImageUrlCount, key, now)
            self.trace("��Ϣ��ҳ��ַ��" + photoAlbumUrl)
            photoAlbumPage = self.doGet(photoAlbumUrl, postData)
            
#             testFile = open('test.txt', 'w')
#             testFile.write(photoAlbumPage)
#             testFile.close()
            
            if photoAlbumPage:
                messageIndex = photoAlbumPage.find('[["https://picasaweb.google.com/' + userId)
                while messageIndex != -1:
                    messageStart = photoAlbumPage.find("http", messageIndex)                   
                    messageStop = photoAlbumPage.find('"', messageStart)
                    messageUrl = photoAlbumPage[messageStart:messageStop]
                    # ����һ��image��URL���浽��id list��
                    if newUserIdList[userId][3] == "":
                        newUserIdList[userId][3] = messageUrl
                    # ����Ƿ������ص�ǰһ�ε�ͼƬ
                    if len(userIdList[userId]) >= 4 and userIdList[userId][3].find("picasaweb.google.com/") != -1:
                        if messageUrl == userIdList[userId][3]:
                            isError = False
                            break
                    self.trace("message URL:" + messageUrl)
                    # �ж��Ƿ��ظ�
                    if messageUrl in messageUrlList:
                        messageIndex = photoAlbumPage.find('[["https://picasaweb.google.com/' + userId, messageIndex + 1)
                        continue
                    messageUrlList.append(messageUrl)
                    messagePage = self.doGet(messageUrl)
                    if not messagePage:
                        self.printErrorMsg("�޷���ȡ��Ϣҳ: " + messageUrl)
                        messageIndex = photoAlbumPage.find('[["https://picasaweb.google.com/' + userId, messageIndex + 1)
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
                        imageUrlList.append(imageUrl)
                        tempList = imageUrl.split("/")
                        # ʹ�����ֱ���
                        tempList[-2] = "s0"
                        imageUrl = "/".join(tempList)
                        # �ļ�����
                        imgByte = self.doGet(imageUrl)
                        fileType = imageUrl.split(".")[-1]
                        imageFile = open(imagePath + "\\" + str("%04d" % imageCount) + "." + fileType, "wb")
                        if imgByte:
                            self.printStepMsg("��ʼ���ص�" + str(imageCount) + "��ͼƬ��" + imageUrl)
                            imageFile.write(imgByte)
                            self.printStepMsg("���سɹ�")
                        else:
                            self.printErrorMsg("��ȡ��" + str(imageCount) + "��ͼƬ��Ϣʧ�ܣ�" + str(userId) + ": " + imageUrl)
                        imageFile.close()
                        imageCount += 1
                        # �ﵽ�����ļ��е���������������
                        if self.getImageCount > 0 and imageCount > self.getImageCount:
                            self.printErrorMsg("�ﵽ������������")
                            break
                        flag = messagePage.find("<div><a href=", flag + 1)
                    messageIndex = photoAlbumPage.find('[["https://picasaweb.google.com/' + userId, messageIndex + 1)
            else:
                self.printErrorMsg("�޷���ȡ�����ҳ: " + photoAlbumUrl + ' ' + userName)
            
            self.printStepMsg(userName + "������ϣ��ܹ����" + str(imageCount - 1) + "��ͼƬ")
            newUserIdList[userId][2] = str(int(newUserIdList[userId][2]) + imageCount - 1)
            totalImageCount += imageCount - 1
            
            # ����
            if self.isSort == 1:
                imageList = sorted(os.listdir(imagePath), reverse=True)
                # �ж�����Ŀ���ļ����Ƿ����
                if len(imageList) >= 1:
                    destPath = self.imageDownloadPath + "\\" + newUserIdList[userId][6] + "\\" + userName
                    if os.path.exists(destPath):
                        if os.path.isdir(destPath):
                            self.printStepMsg("ͼƬ����Ŀ¼��" + destPath + " �Ѵ��ڣ�ɾ����")
                            self.removeDirFiles(destPath)
                        else:
                            self.printStepMsg("ͼƬ����Ŀ¼��" + destPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ����")
                            os.remove(destPath)
                    self.printStepMsg("����ͼƬ����Ŀ¼��" + destPath)
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
            newUserIdListFile = open(newUserIdListFilePath, "a")
            newUserIdListFile.write("\t".join(newUserIdList[userId]) + "\n")
            newUserIdListFile.close()

        # ���򲢱����µ�idList.txt
        tempList = []
        tempUserIdList = sorted(newUserIdList.keys())
        for index in tempUserIdList:
            tempList.append("\t".join(newUserIdList[index]))
        newUserIdListString = "\n".join(tempList)
        newUserIdListFilePath = os.getcwd() + "\\info\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(self.userIdListFilePath)[-1]
        self.printStepMsg("�����´浵�ļ���" + newUserIdListFilePath)
        newUserIdListFile = open(newUserIdListFilePath, "w")
        newUserIdListFile.write(newUserIdListString)
        newUserIdListFile.close()
        
        stopTime = time.time()
        self.printStepMsg("�浵�ļ��������û�ͼƬ�ѳɹ����أ���ʱ" + str(int(stopTime - startTime)) + "�룬����ͼƬ" + str(totalImageCount) + "��")

if __name__ == "__main__":
    downloadImage().main()
