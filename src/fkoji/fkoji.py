# -*- coding:GBK  -*-
'''
Created on 2014-2-8

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''
from common import common
import BeautifulSoup
import os
import shutil
import sys
import time
                
class fkoji(common.Tool):
    
    def trace(self, msg):
        super(fkoji, self).trace(msg, self.isShowError, self.traceLogPath)
    
    def printErrorMsg(self, msg):
        super(fkoji, self).printErrorMsg(msg, self.isShowError, self.errorLogPath)
        
    def printStepMsg(self, msg):
        super(fkoji, self).printStepMsg(msg, self.isShowError, self.stepLogPath)
         
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
        self.getImagePageCount = self.getConfig(config, "GET_IMAGE_PAGE_COUNT", 1, 2)
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
        # ͼƬ�����ı���Ŀ¼
        if os.path.exists(self.imageDownloadPath):
            if os.path.isdir(self.imageDownloadPath):
                isDelete = False
                while not isDelete:
                    # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                    input = raw_input(self.getTime() + " ͼƬ����Ŀ¼��" + self.imageDownloadPath + " �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
                    try:
                        input = input.lower()
                        if input in ["y", "yes"]:
                            isDelete = True
                        elif input in ["n", "no"]:
                            self.processExit()
                    except:
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
        # ͼƬ������ʱĿ¼
        if self.isSort == 1:
            if os.path.exists(self.imageTempPath):
                if os.path.isdir(self.imageTempPath):
                    isDelete = False
                    while not isDelete:
                        # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                        input = raw_input(self.getTime() + " ͼƬ������ʱĿ¼��" + self.imageTempPath + " �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
                        try:
                            input = input.lower()
                            if input in ["y", "yes"]:
                                isDelete = True
                            elif input in ["n", "no"]:
                                self.processExit()
                        except:
                            pass
                    self.printStepMsg("ɾ��ͼƬ������ʱĿ¼��" + self.imageTempPath)
                    shutil.rmtree(self.imageTempPath, True)
                    # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                    while os.path.exists(self.imageTempPath):
                        shutil.rmtree(self.imageTempPath, True)
                        time.sleep(5)
                else:
                    self.printStepMsg("ͼƬ������ʱĿ¼��" + self.imageTempPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
                    os.remove(self.imageTempPath)
            self.printStepMsg("����ͼƬ������ʱĿ¼��" + self.imageTempPath)
            if not self.createDir(self.imageTempPath):
                self.printErrorMsg("����ͼƬ������ʱĿ¼��" + self.imageTempPath + " ʧ�ܣ����������")
                self.processExit()
        # ���ô���
        if self.isProxy == 1:
            self.proxy(self.proxyIp, self.proxyPort, "http")
        saveFilePath = os.getcwd() + "\\" + ".".join(sys.argv[0].split("\\")[-1].split(".")[:-1]) + ".save"
        lastImageUrl = ""
        imageStartIndex = 0
        userIdList = {}
        if os.path.exists(saveFilePath):
            saveFile = open(saveFilePath, "r")
            lines = saveFile.readlines()
            saveFile.close()
            if len(lines) >= 1:
                info = lines[0].split("\t")
                if len(info) >= 2:
                    imageStartIndex = int(info[0])
                    lastImageUrl = info[1].replace("\n", "")
                for line in lines[1:]:
                    line = line.lstrip().rstrip().replace(" ", "")
                    info = line.split("\t")
                    if len(info) >= 2:
                        userIdList[info[0]] = info[1]
        # ����
        url = "http://jigadori.fkoji.com/?p=%s"
        pageIndex = 1
        imageCount = 1
        isOver = False
        newLastImageUrl = ""
        imageUrlList = []
        if self.isSort == 1:
            imagePath = self.imageTempPath
        else:
            imagePath = self.imageDownloadPath
        while True:
            if isOver:
                break
            # �ﵽ�����ļ��е���������������
            if self.getImagePageCount != 0 and pageIndex > self.getImagePageCount:
                break
            indexUrl = url % str(pageIndex)
            self.trace("��ҳ��ַ��" + indexUrl)
            indexPage = self.doGet(indexUrl)
            indexPage = BeautifulSoup.BeautifulSoup(indexPage)
     
            photoList = indexPage.body.findAll("div", "photo")
            # �Ѿ����ص����һҳ
            if not photoList:
                break
            for photoInfo in photoList:
                if isinstance(photoInfo, BeautifulSoup.NavigableString):
                    continue
                tags = photoInfo.findAll("a")
                userId = ""
                imageUrl = ""
                for tag in tags:
                    subTag = tag.next
                    # user id
                    if isinstance(subTag, BeautifulSoup.NavigableString):
                        if subTag.find("@") == 0:
                            userId = subTag[1:]
                    # image url
                    elif isinstance(subTag, BeautifulSoup.Tag):
                        subTagAttrs = dict(subTag.attrs)
                        if subTagAttrs.has_key("src") and subTagAttrs.has_key("alt"):
                            imageUrl = str(subTagAttrs["src"]).replace(" ", "")
                            lastImageUrl = lastImageUrl.replace(" ", "")
                            if newLastImageUrl == "":
                                newLastImageUrl = imageUrl
                            # ����Ƿ������ص�ǰһ�ε�ͼƬ
                            if lastImageUrl == imageUrl:
                                isOver = True
                                break
                if isOver:
                    break
                self.trace("id: " + userId + "����ַ: " + imageUrl)
                if imageUrl in imageUrlList:
                    continue
                imageUrlList.append(imageUrl)
                imgByte = self.doGet(imageUrl)
                fileType = imageUrl.split(".")[-1]
                if fileType.find('/') != -1:
                    fileType = 'jpg'
                imageFile = open(imagePath + "\\" + str("%05d" % imageCount) + "_" + str(userId) + "." + fileType, "wb")
                if imgByte:
                    self.printMsg("��ʼ���ص�" + str(imageCount) + "��ͼƬ��" + imageUrl)
                    imageFile.write(imgByte)
                    self.printMsg("���سɹ�")
                else:
                    self.printErrorMsg("��ȡͼƬ" + str(imageCount) + "��Ϣʧ�ܣ�" + imageUrl)
                imageFile.close()
                imageCount += 1
            pageIndex += 1   
        self.printStepMsg("�������")

        # �����Ƶ�����Ŀ¼
        if self.isSort == 1:
            isCheckOk = False
            while not isCheckOk:
                # �ȴ��ֶ��������ͼƬ����
                input = raw_input(self.getTime() + " �Ѿ�������ϣ��Ƿ���һ�������� (Y)es or (N)o: ")
                try:
                    input = input.lower()
                    if input in ["y", "yes"]:
                        isCheckOk = True
                    elif input in ["n", "no"]:
                        self.processExit()
                except:
                    pass
            if not self.createDir(self.imageDownloadPath + "\\all"):
                self.printErrorMsg("����ͼƬ����Ŀ¼��" + self.imageDownloadPath + "\\all" + " ʧ�ܣ����������")
                self.processExit()
            for fileName in sorted(os.listdir(self.imageTempPath), reverse=True):
                imageStartIndex += 1
                imagePath = self.imageTempPath + "\\" + fileName
                fileNameList = fileName.split(".")
                fileType = fileNameList[-1]
                userId = "_".join(".".join(fileNameList[:-1]).split("_")[1:])
                # ����
                shutil.copyfile(imagePath, self.imageDownloadPath + "\\all\\" + str("%05d" % imageStartIndex) + "_" + userId + "." + fileType)
                # ����
                eachUserPath = self.imageDownloadPath + "\\" + userId
                if not os.path.exists(eachUserPath):
                    if not self.createDir(eachUserPath):
                        self.printErrorMsg("��������ͼƬ����Ŀ¼��" + eachUserPath + " ʧ�ܣ����������")
                        self.processExit()
                if userIdList.has_key(userId):
                    userIdList[userId] = int(userIdList[userId]) + 1
                else:
                    userIdList[userId] = 1
                shutil.copyfile(imagePath, eachUserPath + "\\" + str("%05d" % userIdList[userId]) + "." + fileType)
            self.printStepMsg("ͼƬ������Ŀ¼�ƶ�������Ŀ¼�ɹ�")
            # ɾ��������ʱĿ¼�е�ͼƬ
            shutil.rmtree(self.imageTempPath, True)
            
        # �����µĴ浵�ļ�
        newSaveFilePath = os.getcwd() + "\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(saveFilePath)[-1]
        self.printStepMsg("�����´浵�ļ�: " + newSaveFilePath)
        newSaveFile = open(newSaveFilePath, "w")
        newSaveFile.write(str(imageStartIndex) + "\t" + newLastImageUrl + "\n")
        tempList = []
        tempUserIdList = sorted(userIdList.keys())
        for userId in tempUserIdList:
            tempList.append(userId + "\t" + str(userIdList[userId]))
        newUserIdListString = "\n".join(tempList)
        newSaveFile.write(newUserIdListString)
        newSaveFile.close()
        stopTime = time.time()
        self.printStepMsg("�ɹ���������ͼƬ����ʱ" + str(int(stopTime - startTime)) + "�룬����ͼƬ" + str(imageCount - 1) + "��")

if __name__ == "__main__":
    fkoji().main()
