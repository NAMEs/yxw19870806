# -*- coding:GBK  -*-
'''
Created on 2013-12-15

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

from common import common
import os
import shutil
import time

class weibo(common.Tool):

    def trace(self, msg):
        super(weibo, self).trace(msg, self.isShowError, self.traceLogPath)
    
    def printErrorMsg(self, msg):
        super(weibo, self).printErrorMsg(msg, self.isShowError, self.errorLogPath)
        
    def printStepMsg(self, msg):
        super(weibo, self).printStepMsg(msg, self.isShowError, self.stepLogPath)

    def printMsg(self, msg, isTime=True):
        if isTime:
            msg = self.getTime() + " " + msg
        print msg
        
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
        self.traceLogPath = self.getConfig(config, "TRACE_LOG_FILE_NAME", "\\log\\traceLog.txt", 3)
        self.stepLogPath = self.getConfig(config, "STEP_LOG_FILE_NAME", "\\log\\stepLog.txt", 3)
        self.imageDownloadPath = self.getConfig(config, "IMAGE_DOWNLOAD_DIR_NAME", "\\photo", 3)
        self.printMsg("�����ļ���ȡ���")
            
    def main(self):
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
        
        url = "http://twintail-japan.com/campus/contents/%s.html"
        imageUrl = "http://twintail-japan.com/campus/contents/%s"
        allImageCount = 0
        for pageNumber in range(56, 80):
            page = self.doGet(url % pageNumber)
            if not page:
                self.printMsg("���ؽ���")
                self.processExit()
            nameStart = page.find("��ǰ /")
            nameStop = page.find("(", nameStart)
            name = page[nameStart + 9:nameStop].replace(" ", "").replace("\n", "").decode("utf-8")
            self.trace("ҳ���ַ:" + url % pageNumber)
            self.printMsg("���֣�" + name)
            imagePath = self.imageDownloadPath + "\\" + ("%02d" % pageNumber) + " " + name
            if os.path.exists(imagePath):
                shutil.rmtree(imagePath, True)
            if not self.createDir(imagePath):
                self.printErrorMsg("����ͼƬ����Ŀ¼��" + imagePath + " ʧ�ܣ����������")
                self.processExit()
            imageCount = 1
            if page == False:
                break
            imageStart = page.find("<span>")
            while imageStart != -1:
                imageStop = page.find("</span>", imageStart)
                imageUrlPath = page[imageStart + 6:imageStop]
                imgByte = self.doGet(imageUrl % imageUrlPath)
                if imgByte:
                    fileType = (imageUrl % imageUrlPath).split(".")[-1]
                    imageFile = open(imagePath + "\\" + str("%02d" % imageCount) + "." + fileType, "wb")
                    self.printMsg("��ʼ���ص�" + str(imageCount) + "��ͼƬ��" + imageUrl % imageUrlPath)
                    imageFile.write(imgByte)
                    imageFile.close()
                    self.printMsg("���سɹ�")
                    imageCount += 1
                imageStart = page.find("<span>", imageStart + 1)
            allImageCount += imageCount

if __name__ == "__main__":
    weibo().main()
