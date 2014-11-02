# -*- coding:GBK  -*-
'''
Created on 2013-4-8

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

from common import common, json
import copy
import os
import shutil
import time

class instagram(common.Tool):
    
    def trace(self, msg):
        super(instagram, self).trace(msg, self.isShowError, self.traceLogPath)
    
    def printErrorMsg(self, msg):
        super(instagram, self).printErrorMsg(msg, self.isShowError, self.errorLogPath)
        
    def printStepMsg(self, msg):
        super(instagram, self).printStepMsg(msg, self.isShowError, self.stepLogPath)
         
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
            # ·����Ŀ¼
            if os.path.isdir(self.imageDownloadPath):
                # Ŀ¼��Ϊ��
                if os.listdir(self.imageDownloadPath):
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
            self.proxy(self.proxyIp, self.proxyPort, "http")
        # Ѱ��idlist�����û�н�������
        userIdList = {}
        if os.path.exists(self.userIdListFilePath):
            userListFile = open(self.userIdListFilePath, "r")
            allUserList = userListFile.readlines()
            userListFile.close()
            for userInfo in allUserList:
                if len(userInfo) < 2:
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
        for newUserAccount in newUserIdList:
            # ���û�г�ʼimage count����Ϊ0
            if len(newUserIdList[newUserAccount]) < 2:
                newUserIdList[newUserAccount].append("0")
            # ������һ��image id
            # ���ÿմ�ű��ε�һ�Ż�ȡ��image URL
            if len(newUserIdList[newUserAccount]) < 3:
                newUserIdList[newUserAccount].append("")
            else:
                newUserIdList[newUserAccount][2] = ""
        allImageCount = 0
        # ѭ������ÿ��id
        for userAccount in sorted(userIdList.keys()):
            self.printStepMsg("Account: " + userAccount)
            # ��ʼ������
            imageId = ""
            imageCount = 1
            isPass = False
            # ����д浵��¼����ֱ���ҵ���ǰһ��һ�µĵ�ַ�����������쳣
            if len(userIdList[userAccount]) > 2 and int(userIdList[userAccount][1]) != 0 and userIdList[userAccount][2] != "":
                isError = True
            else:
                isError = False
            # �����Ҫ����������ʹ����ʱ�ļ��У�����ֱ�����ص�Ŀ��Ŀ¼
            if self.isSort == 1:
                imagePath = self.imageTempPath
            else:
                imagePath = self.imageDownloadPath + "\\" + userAccount
            if not self.createDir(imagePath):
                self.printErrorMsg("����ͼƬ����Ŀ¼�� " + imagePath + " ʧ�ܣ����������")
                self.processExit()
            # ͼƬ����
            while 1:
                if isPass:
                    break
                if imageId == "":
                    photoAlbumUrl = "http://instagram.com/%s/media" % userAccount
                else:
                    photoAlbumUrl = "http://instagram.com/%s/media?max_id=%s" % (userAccount, imageId)
                photoAlbumPage = self.doGet(photoAlbumUrl)
                if not photoAlbumPage:
                    self.printErrorMsg("�޷���ȡ�����Ϣ: " + photoAlbumUrl)
                    break
                photoAlbumData = self.doGet(photoAlbumUrl)
                try:
                    photoAlbumPage = json.read(photoAlbumData)
                except:
                    self.printErrorMsg("������Ϣ��" + str(photoAlbumData) + " ����һ��JSON����, user id: " + str(userAccount))
                    break
                if not isinstance(photoAlbumPage, dict):
                    self.printErrorMsg("JSON���ݣ�" + str(photoAlbumPage) + " ����һ���ֵ�, user id: " + str(userAccount))
                    break
                if not photoAlbumPage.has_key("items"):
                    self.printErrorMsg("��JSON���ݣ�" + str(photoAlbumPage) + " ��û���ҵ�'items'�ֶ�, user id: " + str(userAccount))
                    break
                # ���ص������һ��ͼ��
                if photoAlbumPage["items"] == []:
                    break
                for photoInfo in photoAlbumPage["items"]:
                    if not photoInfo.has_key("images"):
                        self.printErrorMsg("��JSON���ݣ�" + str(photoInfo) + " ��û���ҵ�'images'�ֶ�, user id: " + str(userAccount))
                        break
                    if not photoInfo.has_key("id"):
                        self.printErrorMsg("��JSON���ݣ�" + str(photoInfo) + " ��û���ҵ�'id'�ֶ�, user id: " + str(userAccount))
                        break
                    else:
                        imageId = photoInfo["id"]
                    # ����һ��image��id���浽��id list��
                    if newUserIdList[userAccount][2] == "":
                        newUserIdList[userAccount][2] = imageId
                    # ����Ƿ������ص�ǰһ�ε�ͼƬ
                    if len(userIdList[userAccount]) >= 3 and userIdList[userAccount][2].find("_") != -1:
                        if imageId == userIdList[userAccount][2]:
                            isPass = True
                            isError = False
                            break
                    if not photoInfo["images"].has_key("standard_resolution"):
                        self.printErrorMsg("��JSON���ݣ�" + str(photoInfo["images"]) + " ��û���ҵ�'standard_resolution'�ֶ�, user id: " + str(userAccount) + ", image id: " + imageId)
                        break
                    if not photoInfo["images"]["standard_resolution"].has_key("url"):
                        self.printErrorMsg("��JSON���ݣ�" + str(photoInfo["images"]["standard_resolution"]) + " ��û���ҵ�'url'�ֶ�, user id: " + str(userAccount) + ", image id: " + imageId)
                        break
                    imageUrl = photoInfo["images"]["standard_resolution"]["url"]
                    self.trace("image URL:" + imageUrl)
                    imgByte = self.doGet(imageUrl)
                    # �ļ�����
                    fileType = imageUrl.split(".")[-1]
                    # ����ͼƬ
                    filename = str("%04d" % imageCount)
                    imageFile = open(imagePath + "\\" + str(filename) + "." + fileType, "wb")
                    if imgByte:
                        self.printStepMsg("��ʼ���ص�" + str(imageCount) + "��ͼƬ��" + imageUrl)
                        imageFile.write(imgByte)
                        self.printStepMsg("���سɹ�")
                    else:
                        self.printErrorMsg("��ȡͼƬ" + str(imageCount) + "��Ϣʧ�ܣ�" + str(userAccount) + "��" + imageUrl)
                    imageFile.close()
                    imageCount += 1
                    # �ﵽ�����ļ��е���������������
                    if self.getImageCount > 0 and imageCount > self.getImageCount:
                        isPass = True
                        isError = False
                        break
            self.printStepMsg(userAccount + "������ϣ��ܹ����" + str(imageCount - 1) + "��ͼƬ")
            newUserIdList[userAccount][1] = str(int(newUserIdList[userAccount][1]) + imageCount - 1)
            allImageCount += imageCount - 1
            
            # ����
            if self.isSort == 1:
                imageList = sorted(os.listdir(imagePath), reverse=True)
                # �ж�����Ŀ���ļ����Ƿ����
                if len(imageList) >= 1:
                    destPath = self.imageDownloadPath + "\\" + userAccount
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
                    if len(userIdList[userAccount]) >= 3:
                        count = int(userIdList[userAccount][1]) + 1
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
                self.printErrorMsg(userAccount + "ͼƬ�����쳣�����ֶ����")

            # ����������Ϣ
            newUserIdListFile = open(newUserIdListFilePath, "a")
            newUserIdListFile.write("\t".join(newUserIdList[userAccount]) + "\n")
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
        self.printStepMsg("�浵�ļ��������û�ͼƬ�ѳɹ����أ���ʱ" + str(int(stopTime - startTime)) + "�룬����ͼƬ" + str(allImageCount) + "��")

if __name__ == "__main__":
    instagram().main()
