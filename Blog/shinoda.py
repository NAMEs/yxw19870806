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

class Shinoda(common.Tool):

    def trace(self, msg):
        super(Shinoda, self).trace(msg, self.isShowError, self.traceLogPath)
    
    def print_error_msg(self, msg):
        super(Shinoda, self).print_error_msg(msg, self.isShowError, self.errorLogPath)
        
    def print_step_msg(self, msg):
        super(Shinoda, self).print_step_msg(msg, self.isShowError, self.stepLogPath)

    def download(self, imageUrl, imagePath, imageCount):
        imgByte = self.do_get(imageUrl)
        fileType = imageUrl.split(".")[-1]
        imageFile = open(imagePath + "\\" + str("%05d" % imageCount) + "." + fileType, "wb")
        if imgByte:
            self.print_msg(u"��ʼ���ص�" + str(imageCount) + u"��ͼƬ��" + imageUrl)
            imageFile.write(imgByte)
            self.print_msg(u"���سɹ�")
        else:
            self.print_error_msg(u"��ȡͼƬ��Ϣʧ�ܣ�" + imageUrl)
        imageFile.close()
                           
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
                    self.print_msg(str(e))
                    pass
        # ��������
        self.isLog = self.get_config(config, "IS_LOG", 1, 2)
        self.isShowError = self.get_config(config, "IS_SHOW_ERROR", 1, 2)
        self.isDebug = self.get_config(config, "IS_DEBUG", 1, 2)
        self.isShowStep = self.get_config(config, "IS_SHOW_STEP", 1, 2)
        self.isSort = self.get_config(config, "IS_SORT", 1, 2)
        self.getImagePageCount = self.get_config(config, "GET_IMAGE_PAGE_COUNT", 1, 2)
        # ����
        self.isProxy = self.get_config(config, "IS_PROXY", 2, 2)
        self.proxyIp = self.get_config(config, "PROXY_IP", "127.0.0.1", 0)
        self.proxyPort = self.get_config(config, "PROXY_PORT", "8087", 0)
        # �ļ�·��
        self.errorLogPath = self.get_config(config, "ERROR_LOG_FILE_NAME", "\\log\\errorLog.txt", 3)
        if self.isLog == 0:
            self.traceLogPath = ""
            self.stepLogPath = ""
        else:
            self.traceLogPath = self.get_config(config, "TRACE_LOG_FILE_NAME", "\\log\\traceLog.txt", 3)
            self.stepLogPath = self.get_config(config, "STEP_LOG_FILE_NAME", "\\log\\stepLog.txt", 3)
        self.imageDownloadPath = self.get_config(config, "IMAGE_DOWNLOAD_DIR_NAME", "\\photo", 3)
        self.imageTempPath = self.get_config(config, "IMAGE_TEMP_DIR_NAME", "\\tempImage", 3)
        self.print_msg(u"�����ļ���ȡ���")
    
    def main(self):
        startTime = time.time()
        # �жϸ���Ŀ¼�Ƿ����
        # ��־�ļ�����Ŀ¼
        if self.isLog == 1:
            stepLogDir = os.path.dirname(self.stepLogPath)
            if not os.path.exists(stepLogDir):
                self.print_step_msg("������־Ŀ¼�����ڣ������ļ��У�" + stepLogDir)
                if not self.createDir(stepLogDir):
                    self.print_error_msg("����������־Ŀ¼��" + stepLogDir + " ʧ�ܣ����������")
                    self.process_exit()
            traceLogDir = os.path.dirname(self.traceLogPath)
            if not os.path.exists(traceLogDir):
                self.print_step_msg("������־Ŀ¼�����ڣ������ļ��У�" + traceLogDir)
                if not self.createDir(traceLogDir):
                    self.print_error_msg("����������־Ŀ¼��" + traceLogDir + " ʧ�ܣ����������")
                    self.process_exit()
        errorLogDir = os.path.dirname(self.errorLogPath)
        if not os.path.exists(errorLogDir):
            self.print_step_msg("������־Ŀ¼�����ڣ������ļ��У�" + errorLogDir)
            if not self.createDir(errorLogDir):
                self.print_error_msg("����������־Ŀ¼��" + errorLogDir + " ʧ�ܣ����������")
                self.process_exit()
        # ͼƬ�����ı���Ŀ¼
        if os.path.exists(self.imageDownloadPath):
            # ·����Ŀ¼
            if os.path.isdir(self.imageDownloadPath):
                # Ŀ¼��Ϊ��
                if os.listdir(self.imageDownloadPath):
                    isDelete = False
                    while not isDelete:
                        # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                        input = raw_input(self.get_time() + u" ͼƬ����Ŀ¼��" + self.imageDownloadPath + u" �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
                        try:
                            input = input.lower()
                            if input in ["y", "yes"]:
                                isDelete = True
                            elif input in ["n", "no"]:
                                self.process_exit()
                        except:
                            pass
                    self.print_step_msg(u"ɾ��ͼƬ����Ŀ¼��" + self.imageDownloadPath)
                    # ɾ��Ŀ¼
                    shutil.rmtree(self.imageDownloadPath, True)
                    # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                    while os.path.exists(self.imageDownloadPath):
                        shutil.rmtree(self.imageDownloadPath, True)
                        time.sleep(5)
            else:
                self.print_step_msg(u"ͼƬ����Ŀ¼��" + self.imageDownloadPath + u"�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
                os.remove(self.imageDownloadPath)
        self.print_step_msg(u"����ͼƬ����Ŀ¼��" + self.imageDownloadPath)
        if not self.createDir(self.imageDownloadPath):
            self.print_error_msg(u"����ͼƬ����Ŀ¼��" + self.imageDownloadPath + u" ʧ�ܣ����������")
            self.process_exit()
        # ͼƬ������ʱĿ¼
        if os.path.exists(self.imageTempPath):
            if os.path.isdir(self.imageTempPath):
                # Ŀ¼��Ϊ��
                if os.listdir(self.imageTempPath):
                    isDelete = False
                    while not isDelete:
                        # �ֶ������Ƿ�ɾ�����ļ����е�Ŀ¼
                        input = raw_input(self.get_time() + u" ͼƬ������ʱĿ¼��" + self.imageTempPath + u" �Ѿ����ڣ��Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
                        try:
                            input = input.lower()
                            if input in ["y", "yes"]:
                                isDelete = True
                            elif input in ["n", "no"]:
                                self.process_exit()
                        except:
                            pass
                    self.print_step_msg(u"ɾ��ͼƬ������ʱĿ¼��" + self.imageTempPath)
                    shutil.rmtree(self.imageTempPath, True)
                    # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                    while os.path.exists(self.imageTempPath):
                        shutil.rmtree(self.imageTempPath, True)
                        time.sleep(5)
            else:
                self.print_step_msg(u"ͼƬ������ʱĿ¼��" + self.imageTempPath + u"�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
                os.remove(self.imageTempPath)
        self.print_step_msg(u"����ͼƬ������ʱĿ¼��" + self.imageTempPath)
        if not self.createDir(self.imageTempPath):
            self.print_error_msg(u"����ͼƬ������ʱĿ¼��" + self.imageTempPath + u" ʧ�ܣ����������")
            self.process_exit()
        # ���ô���
        if self.isProxy == 1 or self.isProxy == 2:
            self.set_proxy(self.proxyIp, self.proxyPort, "http")
        # ��ȡ�浵�ļ�
        saveFilePath = os.getcwd() + "\\" + ".".join(sys.argv[0].split("\\")[-1].split(".")[:-1]) + ".save"
        lastImageUrl = ""
        imageStartIndex = 0
        if os.path.exists(saveFilePath):
            saveFile = open(saveFilePath, "r")
            saveInfo = saveFile.read()
            saveFile.close()
            saveList = saveInfo.split("\t")
            if len(saveList) >= 2:
                imageStartIndex = int(saveList[0])
                lastImageUrl = saveList[1]
        # ����
        
        pageIndex = 1
        imageCount = 1
        isOver = False
        newLastImageUrl = ""
        while True:
            if isOver:
                break
            indexUrl = "http://blog.mariko-shinoda.net/page%s.html" % (pageIndex - 1)
            indexPage = self.do_get(indexUrl)
            self.trace(u"����ҳ���ַ��" + indexUrl)
            if indexPage:
                # old image:
                imageIndex = 0
                while True:
                    imageIndex = indexPage.find('<a href="http://mariko-shinoda.up.seesaa.net', imageIndex)
                    if imageIndex == -1:
                        break
                    imageStart = indexPage.find("http", imageIndex) 
                    imageStop = indexPage.find('"', imageStart)
                    imageUrl = indexPage[imageStart:imageStop]
                    self.trace(u"ͼƬ��ַ��" + imageUrl)
                    if imageUrl.find("data") == -1:
                        if newLastImageUrl == "":
                            newLastImageUrl = imageUrl
                        # ����Ƿ������ص�ǰһ�ε�ͼƬ
                        if lastImageUrl == imageUrl:
                            isOver = True
                            break
                        # ����ͼƬ
                        self.download(imageUrl, self.imageTempPath, imageCount)
                        imageCount += 1
                    imageIndex += 1
                if isOver:
                    break
                # new image:
                imgTagStart = 0
                while True:
                    imgTagStart = indexPage.find("<img ", imgTagStart)
                    if imgTagStart == -1:
                        break
                    imgTagStop = indexPage.find("/>", imgTagStart)
                    imageIndex = indexPage.find('src="http://blog.mariko-shinoda.net', imgTagStart, imgTagStop)
                    if imageIndex == -1:
                        imgTagStart += 1  
                        continue
                    imageStart = indexPage.find("http", imageIndex)
                    imageStop = indexPage.find('"', imageStart)
                    imageUrl = indexPage[imageStart:imageStop]
                    self.trace(u"ͼƬ��ַ��" + imageUrl)
                    if imageUrl.find("data") == -1:
                        if newLastImageUrl == "":
                            newLastImageUrl = imageUrl
                        # ����Ƿ������ص�ǰһ�ε�ͼƬ
                        if lastImageUrl == imageUrl:
                            isOver = True
                            break
                        # ����ͼƬ
                        self.download(imageUrl, self.imageTempPath, imageCount)
                        imageCount += 1
                    imgTagStart += 1
                if isOver:
                    break
            else:
                break
            pageIndex += 1
            # �ﵽ�����ļ��е���������������
            if self.getImagePageCount != 0 and pageIndex > self.getImagePageCount:
                break
        
        self.print_step_msg(u"�������")
        
        # �����Ƶ�����Ŀ¼
        if self.isSort == 1:
            allImageCount = 0
            for fileName in sorted(os.listdir(self.imageTempPath), reverse=True):
                imageStartIndex += 1
                imagePath = self.imageTempPath + "\\" + fileName
                fileType = fileName.split(".")[-1]
                self.copy_files(imagePath, self.imageDownloadPath + "\\" + str("%05d" % imageStartIndex) + "." + fileType)
                allImageCount += 1
            self.print_step_msg(u"ͼƬ������Ŀ¼�ƶ�������Ŀ¼�ɹ�")
            # ɾ��������ʱĿ¼�е�ͼƬ
            shutil.rmtree(self.imageTempPath, True)
            
        # �����µĴ浵�ļ�
        newSaveFilePath = os.getcwd() + "\\" + time.strftime("%Y-%m-%d_%H_%M_%S_", time.localtime(time.time())) + os.path.split(saveFilePath)[-1]
        self.print_step_msg(u"�����´浵�ļ�: " + newSaveFilePath)
        newSaveFile = open(newSaveFilePath, "w")
        newSaveFile.write(str(imageStartIndex) + "\t" + newLastImageUrl)
        newSaveFile.close()
            
        stopTime = time.time()
        self.print_step_msg(u"�ɹ���������ͼƬ����ʱ" + str(int(stopTime - startTime)) + u"�룬����ͼƬ" + str(imageCount - 1) + u"��")

if __name__ == "__main__":
    Shinoda().main()
