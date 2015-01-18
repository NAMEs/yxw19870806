# -*- coding:GBK  -*-
'''
Created on 2013-8-28

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

import copy
import md5
import os
import random
import shutil
import time

from common import common, json


class weibo(common.Tool):
    
    def trace(self, msg):
        super(weibo, self).trace(msg, self.isShowError, self.traceLogPath)
    
    def printErrorMsg(self, msg):
        super(weibo, self).printErrorMsg(msg, self.isShowError, self.errorLogPath)
        
    def printStepMsg(self, msg):
        super(weibo, self).printStepMsg(msg, self.isShowError, self.stepLogPath)
        
    def visit(self, url):
        tempPage = self.doGet(url)
        if tempPage:
            redirectUrlIndex = tempPage.find("location.replace")           
            if redirectUrlIndex != -1:
                redirectUrlStart = tempPage.find("'", redirectUrlIndex) + 1
                redirectUrlStop = tempPage.find("'", redirectUrlStart)
#                 redirectUrlStart = tempPage.find('"', redirectUrlIndex) + 1
#                 redirectUrlStop = tempPage.find('"', redirectUrlStart)
                redirectUrl = tempPage[redirectUrlStart:redirectUrlStop]
                return str(self.doGet(redirectUrl))
            elif tempPage.find("�û������������") != -1:
                self.printErrorMsg("��½״̬�쳣����������������µ�½΢���˺�")
                self.processExit()
            else:
                try:
                    tempPage = tempPage.decode("utf-8")
                    if tempPage.find("�û������������") != -1:
                        self.printErrorMsg("��½״̬�쳣����������������µ�½΢���˺�")
                        self.processExit()
                except Exception, e:
                    pass
                return str(tempPage)
        return False

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
        # ÿ�������ȡ��ͼƬ����
        self.IMAGE_COUNT_PER_PAGE = 20
        # ��������
        self.isLog = self.getConfig(config, "IS_LOG", 1, 2)
        self.isShowError = self.getConfig(config, "IS_SHOW_ERROR", 1, 2)
        self.isDebug = self.getConfig(config, "IS_DEBUG", 1, 2)
        self.isShowStep = self.getConfig(config, "IS_SHOW_STEP", 1, 2)
        self.isSort = self.getConfig(config, "IS_SORT", 1, 2)
        self.getImageCount = self.getConfig(config, "GET_IMAGE_COUNT", 0, 2)
        # ��������
        self.isProxy = self.getConfig(config, "IS_PROXY", 2, 2)
        self.proxyIp = self.getConfig(config, "PROXY_IP", "127.0.0.1", 0)
        self.proxyPort = self.getConfig(config, "PROXY_PORT", "8087", 0)
        # �ļ�·��
        self.errorLogPath = self.getConfig(config, "ERROR_LOG_FILE_NAME", "\\log\\errorLog.txt", 3)
        if self.isLog == 0:
            self.traceLogPath = ''
            self.stepLogPath = ''
        else:
            self.traceLogPath = self.getConfig(config, "TRACE_LOG_FILE_NAME", "\\log\\traceLog.txt", 3)
            self.stepLogPath = self.getConfig(config, "STEP_LOG_FILE_NAME", "\\log\\stepLog.txt", 3)
        self.imageDownloadPath = os.getcwd() +  "\\photo2"
        self.imageTempPath = os.getcwd() +  "\\photo2\\tempImage"
        self.userIdListFilePath = os.getcwd() + "\\info\\idlist_2.txt"
        # ����ϵͳ&�����
        self.browerVersion = self.getConfig(config, "BROWSER_VERSION", 2, 2)
        self.osVersion = self.getConfig(config, "OS_VERSION", 1, 2)
        # cookie
        self.isAutoGetCookie = self.getConfig(config, "IS_AUTO_GET_COOKIE", 1, 2)
        if self.isAutoGetCookie == 0:
            self.cookiePath = self.getConfig(config, "COOKIE_PATH", "", 0)
        else:
            self.cookiePath = self.getDefaultBrowserCookiePath(self.osVersion, self.browerVersion)
        self.printMsg("�����ļ���ȡ���")
            
    def main(self):
        startTime = time.time()
        # �жϸ���Ŀ¼�Ƿ����
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
                        input = raw_input(self.getTime() + " ͼƬ����Ŀ¼��" + self.imageDownloadPath + " �Ѵ��ڣ��Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
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
                    shutil.rmtree(self.imageDownloadPath, True)
                    # ��������ֹ�ļ�����ɾ��ʱ�������5����һ���ļ����Ƿ��Ѿ�ɾ��
                    while os.path.exists(self.imageDownloadPath):
                        shutil.rmtree(self.imageDownloadPath, True)
                        time.sleep(5)
            else:
                self.printStepMsg("ͼƬ����Ŀ¼��" + self.imageDownloadPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
                os.remove(self.imageDownloadPath)
        if not self.createDir(self.imageDownloadPath):
            self.printErrorMsg("����ͼƬ����Ŀ¼��" + self.imageDownloadPath + " ʧ�ܣ����������")
            self.processExit()
        self.printStepMsg("����ͼƬ����Ŀ¼��" + self.imageDownloadPath)
        # ���ô���
        if self.isProxy == 1:
            self.proxy(self.proxyIp, self.proxyPort, "http")
        # ����ϵͳcookies (fire fox)
        if not self.cookie(self.cookiePath, self.browerVersion):
            self.printErrorMsg("���������cookiesʧ�ܣ����������")
            self.processExit()
        # Ѱ��idlist�����û�н�������
        userIdList = {}
        if os.path.exists(self.userIdListFilePath):
            userListFile = open(self.userIdListFilePath, 'r')
            allUserList = userListFile.readlines()
            userListFile.close()
            for userInfo in allUserList:
                userInfo = userInfo.replace(" ", "")
                userInfo = userInfo.replace("\n", "")
                userInfo = userInfo.replace("\r", "")
                userInfoList = userInfo.split("\t")
                userIdList[userInfoList[0]] = userInfoList
        else:
            self.printErrorMsg("�û�ID�浵�ļ���" + self.userIdListFilePath + "�����ڣ����������")
            self.processExit()
        newUserIdListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.userIdListFilePath)[-1]
        newUserIdListFile = open(newUserIdListFilePath, 'w')
        newUserIdListFile.close()

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
            # �����Ա������Ϣ
            if len(newUserIdList[newUserId]) < 5:
                newUserIdList[newUserId].append("")
        allImageCount = 0
        for userId in sorted(userIdList.keys()):
            userName = newUserIdList[userId][1]
            self.printStepMsg("UID: " + str(userId) + "��Name: " + userName)
            # ��ʼ������
            pageCount = 1
            imageCount = 1
            totalImageCount = 0
            isPass = False
            if len(userIdList[userId]) < 3 or userIdList[userId][3] == '':
                isError = False
            else:
                isError = True
            # �����Ҫ����������ʹ����ʱ�ļ��У�����ֱ�����ص�Ŀ��Ŀ¼\
            if self.isSort == 1:
                imagePath = self.imageTempPath
            else:
                imagePath = self.imageDownloadPath + "\\" + userName
            if os.path.exists(imagePath):
                shutil.rmtree(imagePath, True)
            if not self.createDir(imagePath):
                self.printErrorMsg("����ͼƬ����Ŀ¼��" + imagePath + " ʧ�ܣ����������")
                self.processExit()
            # ��־�ļ�������Ϣ
            while 1:
                photoAlbumUrl = "http://photo.weibo.com/photos/get_all?uid=%s&count=%s&page=%s&type=3" % (userId, self.IMAGE_COUNT_PER_PAGE, pageCount)
                self.trace("���ר����ַ��" + photoAlbumUrl)
                photoPageData = self.visit(photoAlbumUrl)
                self.trace("����JSON���ݣ�" + photoPageData)
                try:
                    page = json.read(photoPageData)
                except:
                    self.printErrorMsg("������Ϣ��" + str(photoPageData) + " ����һ��JSON����, user id: " + str(userId))
                    break
                if not isinstance(page, dict):
                    self.printErrorMsg("JSON���ݣ�" + str(page) + " ����һ���ֵ�, user id: " + str(userId))
                    break
                if not page.has_key("data"):
                    self.printErrorMsg("��JSON���ݣ�" + str(page) + " ��û���ҵ�'data'�ֶ�, user id: " + str(userId))
                    break
                if totalImageCount == 0:
                    if page["data"].has_key("total"):
                        totalImageCount = page["data"]["total"]
                    else:
                        self.printErrorMsg("��JSON���ݣ�" + str(page) + " ��û���ҵ�'total'�ֶ�, user id: " + str(userId))
                        isPass = True
                        break
                if not isinstance(page["data"], dict):
                    self.printErrorMsg("JSON����['data']��" + str(page["data"]) + " ����һ���ֵ�, user id: " + str(userId))
                    break
                if not page["data"].has_key("photo_list"):
                    self.printErrorMsg("��JSON���ݣ�" + str(page["data"]) + " ��û���ҵ�'photo_list'�ֶ�, user id: " + str(userId))
                    break
                for imageInfo in page["data"]["photo_list"]:
                    if not isinstance(imageInfo, dict):
                        self.printErrorMsg("JSON����['photo_list']��" + str(imageInfo) + " ����һ���ֵ�, user id: " + str(userId))
                        continue
                    if imageInfo.has_key("pic_host"):
                        imageUrl = imageInfo["pic_host"]
                    else:
                        imageUrl = "http://ww%s.sinaimg.cn" % str(random.randint(1, 4))
                    if imageInfo.has_key("pic_name"):
                        # ����һ��image��URL���浽��id list��
                        if newUserIdList[userId][3] == "":
                            newUserIdList[userId][3] = imageInfo["pic_name"]
                        # ����Ƿ������ص�ǰһ�ε�ͼƬ
                        if len(userIdList[userId]) >= 4:
                            if imageInfo["pic_name"] == userIdList[userId][3]:
                                isPass = True
                                isError = False
                                break
                        imageUrl += "/large/" + imageInfo["pic_name"]
                    else:
                        self.printErrorMsg("��JSON���ݣ�" + str(imageInfo) + " ��û���ҵ�'pic_name'�ֶ�, user id: " + str(userId))
                    self.printStepMsg("��ʼ���ص�" + str(imageCount) + "��ͼƬ��" + imageUrl)
                    while True:
                        imgByte = self.doGet(imageUrl)
                        if imgByte:
                            md5Digest = md5.new(imgByte).hexdigest()
                            # �����ȡ���ļ�ΪweiboĬ�ϻ�ȡʧ�ܵ�ͼƬ
                            if md5Digest == 'd29352f3e0f276baaf97740d170467d7' or md5Digest == '7bd88df2b5be33e1a79ac91e7d0376b5':
                                self.printStepMsg("Դ�ļ���ȡʧ�ܣ�����")
                            else:
                                fileType = imageUrl.split(".")[-1]
                                if fileType.find('/') != -1:
                                    fileType = 'jpg'
                                imageFile = open(imagePath + "\\" + str("%04d" % imageCount) + "." + fileType, "wb")
                                imageFile.write(imgByte)
                                self.printStepMsg("���سɹ�")
                                imageFile.close()
                                imageCount += 1
                                break
                        else:
                            self.printErrorMsg("����ͼƬʧ�ܣ��û�ID��" + str(userId) + "��ͼƬ��ַ��" + imageUrl)
                            break 
                    # �ﵽ�����ļ��е���������������
                    if self.getImageCount > 0 and imageCount > self.getImageCount:
                        isPass = True
                        break
                if isPass:
                    break
                if totalImageCount / self.IMAGE_COUNT_PER_PAGE > pageCount - 1:
                    pageCount += 1
                else:
                    # ȫ��ͼƬ�������
                    break
            
            self.printStepMsg(userName + "������ϣ��ܹ����" + str(imageCount - 1) + "��ͼƬ")
            newUserIdList[userId][2] = str(int(newUserIdList[userId][2]) + imageCount - 1)
            allImageCount += imageCount - 1
            
            # ����
            if self.isSort == 1:
                imageList = sorted(os.listdir(imagePath), reverse=True)
                # �ж�����Ŀ���ļ����Ƿ����
                if len(imageList) >= 1:
                    destPath = self.imageDownloadPath + "\\" + userName
                    if os.path.exists(destPath):
                        if os.path.isdir(destPath):
                            self.printStepMsg("ͼƬ����Ŀ¼��" + destPath + " �Ѵ��ڣ�ɾ����")
                            self.removeDirFiles(destPath)
                        else:
                            self.printStepMsg("ͼƬ����Ŀ¼��" + destPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
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
            newUserIdListFile = open(newUserIdListFilePath, 'a')
            newUserIdListFile.write("\t".join(newUserIdList[userId]) + "\n")
            newUserIdListFile.close()

        # ���򲢱����µ�idList.txt
        tempList = []
        tempUserIdList = sorted(newUserIdList.keys())
        for index in tempUserIdList:
            tempList.append("\t".join(newUserIdList[index]))
        newUserIdListString = "\n".join(tempList)
        newUserIdListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.userIdListFilePath)[-1]
        self.printStepMsg("�����´浵�ļ���" + newUserIdListFilePath)
        newUserIdListFile = open(newUserIdListFilePath, 'w')
        newUserIdListFile.write(newUserIdListString)
        newUserIdListFile.close()
        
        stopTime = time.time()
        self.printStepMsg("�浵�ļ��������û�ͼƬ�ѳɹ����أ���ʱ" + str(int(stopTime - startTime)) + "�룬����ͼƬ" + str(allImageCount) + "��")

if __name__ == '__main__':
    weibo().main()
