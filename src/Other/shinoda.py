# -*- coding:GBK  -*-
'''
Created on 2013-5-6

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''
from common import common
import os
import shutil
import sys
import time

class shinoda(common.Tool):
    
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

    def download(self, imageUrl, imagePath, imageCount):
        imgByte = self.doGet(imageUrl)
        if imgByte:
            fileType = imageUrl.split(".")[-1]
            imageFile = open(imagePath + "\\" + str("%03d" % imageCount) + "." + fileType, "wb")
            self.printMsg("start download " + str(imageCount) + ": " + imageUrl)
            imageFile.write(imgByte)
            imageFile.close()
            self.printMsg("download succeed")
        else:
            self.printErrorMsg("download image failed: " + imageUrl)
                           
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
        self.errorLogPath = self.getConfig(config, "ERROR_LOG_FILE_NAME", processPath + "\\log\\errorLog.txt", 1, prefix=processPath + "\\")
        self.traceLogPath = self.getConfig(config, "TRACE_LOG_FILE_NAME", processPath + "\\log\\traceLog.txt", 1, prefix=processPath + "\\")
        self.stepLogPath = self.getConfig(config, "STEP_LOG_FILE_NAME", processPath + "\\log\\stepLog.txt", 1, prefix=processPath + "\\")
        self.imageDownloadPath = self.getConfig(config, "IMAGE_DOWNLOAD_DIR_NAME", processPath + "\\photo", 1, prefix=processPath + "\\")
        imageTempDirName = self.getConfig(config, "IMAGE_TEMP_DIR_NAME", "tmpImage", 0)
        self.imageTempPath = os.getcwd() + "\\" + imageTempDirName
        # �����ļ���ȡ��������
        self.isLog = self.getConfig(config, "IS_LOG", 1, 2)
        self.isShowError = self.getConfig(config, "IS_SHOW_ERROR", 1, 2)
        self.isDebug = self.getConfig(config, "IS_DEBUG", 1, 2)
        self.isShowStep = self.getConfig(config, "IS_SHOW_STEP", 1, 2)
        self.isDownloadImage = self.getConfig(config, "IS_DOWNLOAD_IMAGE", 1, 2)
        self.isSort = self.getConfig(config, "IS_SORT", 1, 2)
        self.getImagePageCount = self.getConfig(config, "GET_IMAGE_PAGE_COUNT", 1, 2)
#        self.isProxy = self.getConfig(config, "IS_PROXY", 1, 2)
#        self.proxyIp = self.getConfig(config, "PROXY_IP", "127.0.0.1", 0)
#        self.proxyPort = self.getConfig(config, "PROXY_PORT", "8087", 0)
        self.printMsg("config init succeed")
    
    def main(self):
        # picture
        if self.isDownloadImage != 1:
            self.processExit()
        startTime = time.time()
        # �жϸ���Ŀ¼�Ƿ����
        # ��־�ļ�����Ŀ¼
        if self.isLog == 1:
            stepLogDir = os.path.dirname(self.stepLogPath)
            if not os.path.exists(stepLogDir):
                if not self.createDir(stepLogDir):
                    #self.printErrorMsg("create " + stepLogDir + " error, process stop!")
                    self.printErrorMsg("����������־Ŀ¼��" + stepLogDir + " ʧ�ܣ����������")
                    self.processExit()
                #self.printStepMsg("step log file path is not exist, create it: " + stepLogDir)
                self.printStepMsg("������־Ŀ¼������, �����ļ���: " + stepLogDir)
            errorLogDir = os.path.dirname(self.errorLogPath)
            if not os.path.exists(errorLogDir):
                if not self.createDir(errorLogDir):
                    #self.printErrorMsg("create " + errorLogDir + " error, process stop!")
                    self.printErrorMsg("����������־Ŀ¼��" + errorLogDir + " ʧ�ܣ����������")
                    self.processExit()
                #self.printStepMsg("error log file path is not exist, create it: " + errorLogDir)
                self.printStepMsg("������־Ŀ¼������, �����ļ���: " + errorLogDir)
            traceLogDir = os.path.dirname(self.traceLogPath)
            if not os.path.exists(traceLogDir):
                if not self.createDir(traceLogDir):
                    #self.printErrorMsg("create " + traceLogDir + " error, process stop!")
                    self.printErrorMsg("����������־Ŀ¼��" + traceLogDir + " ʧ�ܣ����������")
                    self.processExit()
                #self.printStepMsg("trace log file path is not exist, create it: " + traceLogDir)
                self.printStepMsg("������־Ŀ¼������, �����ļ���: " + traceLogDir)
        # ͼƬ�����ı���Ŀ¼
        if os.path.exists(self.imageDownloadPath):
            if os.path.isdir(self.imageDownloadPath):
                isDelete = False
                while not isDelete:
                    # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                    #input = raw_input(self.imageDownloadPath + " is exist, do you want to remove it and continue? (Y)es or (N)o: ")
                    input = raw_input("ͼƬ����Ŀ¼��" + self.imageDownloadPath + " �Ѿ�����, �Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
                    try:
                        input = input.lower()
                        if input in ["y", "yes"]:
                            isDelete = True
                        elif input in ["n", "no"]:
                            self.processExit()
                    except:
                        pass
                #self.printStepMsg("image download path: " + self.imageDownloadPath + " is exist, remove it")
                self.printStepMsg("����ɾ��ͼƬ����Ŀ¼: " + self.imageDownloadPath)
                # ɾ��Ŀ¼
                shutil.rmtree(self.imageDownloadPath, True)
                # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                while os.path.exists(self.imageDownloadPath):
                    time.sleep(5)
            else:
                #self.printStepMsg("image download path: " + self.imageDownloadPath + " is a file, delete it")
                self.printStepMsg("ͼƬ����Ŀ¼: " + self.imageDownloadPath + "�Ѵ�����ͬ���ֵ��ļ�, �Զ�ɾ����")
                os.remove(self.imageDownloadPath)
        #self.printStepMsg("created image download path: " + self.imageDownloadPath)
        self.printStepMsg("���ڴ���ͼƬ����Ŀ¼: " + self.imageDownloadPath)
        if not self.createDir(self.imageDownloadPath):
            #self.printErrorMsg("create " + self.imageDownloadPath + " error, process stop!")
            self.printErrorMsg("����ͼƬ����Ŀ¼��" + self.imageDownloadPath + " ʧ�ܣ����������")
            self.processExit()
        # ͼƬ������ʱĿ¼
        if os.path.exists(self.imageTempPath):
            if os.path.isdir(self.imageTempPath):
                isDelete = False
                while not isDelete:
                    # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                    #input = raw_input(self.imageTempPath + " is exist, do you want to remove it and continue? (Y)es or (N)o: ")
                    input = raw_input("ͼƬ������ʱĿ¼��" + self.imageTempPath + " �Ѿ�����, �Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
                    try:
                        input = input.lower()
                        if input in ["y", "yes"]:
                            isDelete = True
                        elif input in ["n", "no"]:
                            self.processExit()
                    except:
                        pass
                #self.printStepMsg("image temp path: " + self.imageTempPath + " is exist, remove it")
                self.printStepMsg("����ɾ��ͼƬ������ʱĿ¼: " + self.imageTempPath)
                shutil.rmtree(self.imageTempPath, True)
                # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                while os.path.exists(self.imageTempPath):
                    time.sleep(5)
            else:
                #self.printStepMsg("image temp path: " + self.imageTempPath + " is a file, delete it")
                self.printStepMsg("ͼƬ������ʱĿ¼: " + self.imageTempPath + "�Ѵ�����ͬ���ֵ��ļ�, �Զ�ɾ����")
                os.remove(self.imageTempPath)
        #self.printStepMsg("created image temp path: " + self.imageTempPath)
        self.printStepMsg("���ڴ���ͼƬ������ʱĿ¼: " + self.imageTempPath)
        if not self.createDir(self.imageTempPath):
            #self.printErrorMsg("create " + self.imageTempPath + " error, process stop!")
            self.printErrorMsg("����ͼƬ������ʱĿ¼��" + self.imageTempPath + " ʧ�ܣ����������")
            self.processExit()
        # ���ô���
        if self.isProxy == 1:
            self.proxy(self.proxyIp, self.proxyPort)
        # ����
        url = "http://blog.mariko-shinoda.net/index%s.html"
        indexCount = 1
        allImageCount = 0
        # ��ȡ�浵�ļ�
        saveFilePath = os.getcwd() + "\\" + ".".join(sys.argv[0].split("\\")[-1].split(".")[:-1]) + ".save"
        if os.path.exists(saveFilePath):
            saveFile = open(saveFilePath, 'r')
            saveInfo = saveFile.read()
            saveFile.close()
            saveList = saveInfo.split("\t")
            lastImageUrl = saveList[0]
            imageStartIndex = saveList[1]
        else:
            lastImageUrl = ""
            imageStartIndex = 0
        isOver = False
        newLastImageUrl = ""
        while True:
            # �ﵽ�����ļ��е���������������
            if self.getImagePageCount != 0 and indexCount > self.getImagePageCount:
                break
            imageCount = 1
            imagePath = self.imageTempPath + "\\" + str("%03d" % indexCount)
            if indexCount > 1:
                indexUrl = url % ("_" + str(indexCount))
                indexPage = self.doGet(indexUrl)
            else:
                indexUrl = url % ("")
                indexPage = self.doGet(indexUrl)
            #self.trace("index URL:" + indexUrl)
            self.trace("����ҳ���ַ:" + indexUrl)
            if indexPage:
                if not os.path.exists(imagePath):
                    os.makedirs(imagePath)
                # old image:
                imageIndex = 0
                while True:
                    imageIndex = indexPage.find('<a href="http://mariko-shinoda.up.seesaa.net', imageIndex)
                    if imageIndex == -1:
                        break
                    imageStart = indexPage.find("http", imageIndex) 
                    imageStop = indexPage.find('"', imageStart)
                    imageUrl = indexPage[imageStart:imageStop]
                    #self.trace("image URL:" + imageUrl)
                    self.trace("ͼƬ��ַ:" + imageUrl)
                    if imageUrl.find("data") == -1:
                        if newLastImageUrl == "":
                            newLastImageUrl = imageUrl
                        # ����Ƿ������ص�ǰһ�ε�ͼƬ
                        if lastImageUrl == imageUrl:
                            isOver = True
                            break
                        # ����ͼƬ
                        self.download(imageUrl, imagePath, imageCount)
                        imageCount += 1
                        allImageCount += 1
                    imageIndex += 1
                # new image:
                if isOver:
                    break
                imageIndex = 0
                while True:
                    imageIndex = indexPage.find('<img src="http://blog.mariko-shinoda.net', imageIndex)
                    if imageIndex == -1:
                        break
                    imageStart = indexPage.find("http", imageIndex)
                    imageStop = indexPage.find('"', imageStart)
                    imageUrl = indexPage[imageStart:imageStop]
                    #self.trace("image URL:" + imageUrl)
                    self.trace("ͼƬ��ַ:" + imageUrl)
                    if imageUrl.find("data") == -1:
                        # ����Ƿ������ص�ǰһ�ε�ͼƬ
                        if lastImageUrl == imageUrl:
                            isOver = True
                            break
                        # ����ͼƬ
                        self.download(imageUrl, imagePath, imageCount)
                        imageCount += 1
                        allImageCount += 1
                    imageIndex += 1   
                if isOver:
                    break       
            else:
                break
            indexCount += 1
        
        #self.printStepMsg("download over!, count: " + str(allImageCount))
        self.printStepMsg("�������,�ܹ����" + str(allImageCount) + "��ͼƬ")
        # �����µĴ浵�ļ�
        newSaveFilePath = os.getcwd() + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(saveFilePath)[-1]
        #self.printStepMsg("save new save file: " + newSaveFilePath)
        self.printStepMsg("�����´浵�ļ�: " + newSaveFilePath)
        newSaveFile = open(newSaveFilePath, 'w')
        newSaveFile.write(lastImageUrl)
        saveFile.close()
        
        # �����Ƶ�����Ŀ¼
        if self.isSort == 1:
            allImageCount = 0
            for index1 in sorted(os.listdir(self.imageTempPath), reverse=True):
                for fileName in sorted(os.listdir(self.imageTempPath + "\\" + index1), reverse=True):
                    imageStartIndex += 1
                    imagePath = self.imageTempPath + "\\" + index1 + "\\" + fileName
                    fileType = fileName.split(".")[-1]
                    shutil.copyfile(imagePath, self.imageDownloadPath + "\\" + str("%05d" % imageStartIndex) + "." + fileType)
                    allImageCount += 1
            #self.printStepMsg("sorted over!��)
            self.printStepMsg("�����ƶ���ͼƬ����Ŀ¼�ɹ�")
            # ɾ��������ʱĿ¼�е�ͼƬ
            shutil.rmtree(self.imageTempPath, True)
            
            
        stopTime = time.time()
        #self.printStepMsg("all members' image download succeed, use " + str(int(stopTime - startTime)) + " seconds, sum download image count: " + str(allImageCount))
        self.printStepMsg("�ɹ���������ͼƬ, ��ʱ" + str(int(stopTime - startTime)) + "��, ����ͼƬ" + str(allImageCount) + "��")

if __name__ == '__main__':
    shinoda().main()
