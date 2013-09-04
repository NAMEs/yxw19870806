# -*- coding:GBK  -*-
'''
Created on 2013-8-28

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

from common import common, json
import copy
import getpass
import os
import random
import shutil
import time

class weibo(common.Tool):
    
    def visit(self, url):
        tempPage = self.doGet(url)
#         try:
#             tempPage = tempPage.decode("utf-8")
#         except:
#             pass
        if tempPage:
            redirectUrlIndex = tempPage.find("location.replace")
            if redirectUrlIndex != -1:
                redirectUrlStart = tempPage.find('"', redirectUrlIndex) + 1
                redirectUrlStop = tempPage.find('"', redirectUrlStart)
                redirectUrl = tempPage[redirectUrlStart:redirectUrlStop]
                return self.doGet(redirectUrl)
            elif tempPage.find("�û������������") != -1:
                self.printErrorMsg("��½״̬�쳣�����ڻ������������µ�½΢���˺�")
                self.processExit()
            else:
                return tempPage
        return False
    
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
        self.errorLogPath = self.getConfig(config, "ERROR_LOG_FILE_NAME", processPath + "\\log\\errorLog.txt", 1, prefix=processPath + "\\")
        self.traceLogPath = self.getConfig(config, "TRACE_LOG_FILE_NAME", processPath + "\\log\\traceLog.txt", 1, prefix=processPath + "\\")
        self.stepLogPath = self.getConfig(config, "STEP_LOG_FILE_NAME", processPath + "\\log\\stepLog.txt", 1, prefix=processPath + "\\")
        self.imageDownloadPath = self.getConfig(config, "IMAGE_DOWNLOAD_DIR_NAME", processPath + "\\photo", 1, prefix=processPath + "\\")
        self.imageTmpDirName = self.getConfig(config, "IMAGE_TEMP_DIR_NAME", "tmpImage", 0)
        self.memberUIdListFilePath = self.getConfig(config, "MEMBER_UID_LIST_FILE_NAME", processPath + "\\idlist.txt", 1, prefix=processPath + "\\")
        self.defaultFFPath = "C:\\Users\\%s\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\" % (getpass.getuser())
        self.browserPath = self.getConfig(config, "FIREFOX_BROWSER_PATH", self.defaultFFPath, 1, postfix="\cookies.sqlite")
        self.defaultCookiePath = ""
        for dirName in os.listdir(self.defaultFFPath):
            if os.path.isdir(self.defaultFFPath + dirName):
                if os.path.exists(self.defaultFFPath + dirName + "\\cookies.sqlite"):
                    defaultFFPath = self.defaultFFPath + dirName
                    self.defaultCookiePath = defaultFFPath + "\\cookies.sqlite"
                    break
        # ÿ�������ȡ��ͼƬ����
        self.IMAGE_COUNT_PER_PAGE = 100
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
        if os.path.exists(self.imageDownloadPath):
            if os.path.isdir(self.imageDownloadPath):
                isDelete = False
                while not isDelete:
                    input = raw_input("ͼƬ����Ŀ¼��" + self.imageDownloadPath + " �Ѵ��ڣ��Ƿ���Ҫɾ�����ļ��в���������? (Y)es or (N)o: ")
                    try:
                        input = input.lower()
                        if input in ["y", "yes"]:
                            isDelete = True
                        elif input in ["n", "no"]:
                            self.processExit()
                    except:
                        pass
                self.printStepMsg("ɾ��ͼƬ����Ŀ¼: " + self.imageDownloadPath)
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
        if self.isProxy == 1:
            self.proxy()
        # ����ϵͳcookies (fire fox)
        if not self.cookie(self.browserPath):
            self.printMsg("ʹ��Ĭ��Fire Fox cookiesĿ¼: " + self.defaultFFPath)
            if not self.cookie(self.defaultCookiePath):
                self.printErrorMsg("����ϵͳFire Fox cookiesʧ�ܣ����������")
                self.processExit()
        # Ѱ��idlist�����û�н�������
        userIdList = {}
        if os.path.exists(self.memberUIdListFilePath):
            userListFile = open(self.memberUIdListFilePath, 'r')
            allUserList = userListFile.readlines()
            userListFile.close()
            for userInfo in allUserList:
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
            # ����member ������Ϣ
            if len(newMemberUidList[newUserId]) < 5:
                newMemberUidList[newUserId].append("")
        allImageCount = 0
        for userId in userIdList:
            userName = newMemberUidList[userId][1]
            self.printStepMsg("UID: " + str(userId) + "��Member: " + userName)
            # ��ʼ������
            pageCount = 1
            imageCount = 1
            totalImageCount = 0
            isPass = False
            isError = False
            # �����Ҫ����������ʹ����ʱ�ļ��У�����ֱ�����ص�Ŀ��Ŀ¼
            if self.isSort == 1:
                imagePath = self.imageDownloadPath + "\\" + self.imageTmpDirName
            else:
                imagePath = self.imageDownloadPath + "\\" + userName
            if not self.createDir(imagePath):
                self.printErrorMsg("����ͼƬ����Ŀ¼��" + imagePath + " ʧ�ܣ����������")
                self.processExit()
            # ��־�ļ�������Ϣ
            while 1:
                if isPass:
                    break
                photoAlbumUrl = "http://photo.weibo.com/photos/get_all?uid=%s&count=%s&page=%s&type=3" % (userId, self.IMAGE_COUNT_PER_PAGE, pageCount)
                self.trace("���ר����ַ��" + photoAlbumUrl)
                photoPageData = self.visit(photoAlbumUrl)
                self.trace("����JSON���ݣ�" + photoPageData)
                page = json.read(photoPageData)
                if page.has_key("data"):
                    if totalImageCount == 0:
                        if page["data"].has_key("total"):
                            totalImageCount = page["data"]["total"]
                        else:
                            self.printErrorMsg("��JSON���ݣ�" + page + " ��û���ҵ�'total'�ֶ�")
                            isPass = True
                            break
                    if page["data"].has_key("photo_list"):
                        for imageInfo in page["data"]["photo_list"]:
                            if imageInfo.has_key("pic_host"):
                                imageUrl = imageInfo["pic_host"]
                            else:
                                imageUrl = "http://ww%s.sinaimg.cn" % str(random.randint(1, 3))
                            if imageInfo.has_key("pic_name"):
                                imageUrl += "/large/" + imageInfo["pic_name"]
                            else:
                                self.printErrorMsg("��JSON���ݣ�" + imageInfo + " ��û���ҵ�'pic_name'�ֶ�")
                            # ����һ��image��URL���浽��id list��
                            if newMemberUidList[userId][3] == "":
                                newMemberUidList[userId][3] = imageUrl
                            # ����Ƿ������ص�ǰһ�ε�ͼƬ
                            if len(userIdList[userId]) >= 4 and userIdList[userId][3].find("picasaweb.google.com/"):
                                if imageUrl == userIdList[userId][3]:
                                    isPass = True
                                    break
                            self.printStepMsg("��ʼ���ص�" + str(imageCount) + "��ͼƬ��" + imageUrl)
                            imgByte = self.doGet(imageUrl)
                            if imgByte:
                                fileType = imageUrl.split(".")[-1]
                                filename = str("%04d" % imageCount)
                                imageFile = open(imagePath + "\\" + str(filename) + "." + fileType, "wb")
                                imageFile.write(imgByte)
                                imageFile.close()
                                self.printStepMsg("���سɹ�")
                                imageCount += 1
                            else:
                                self.printErrorMsg("����ͼƬʧ�ܣ��û�ID��" + str(userId) + "��ͼƬ��ַ: " + imageUrl)
                    else:
                        self.printErrorMsg("��JSON���ݣ�" + page + " ��û���ҵ�'photo_list'�ֶ�")
                else:
                    self.printErrorMsg("��JSON���ݣ�" + page + " ��û���ҵ�'data'�ֶ�")
                if totalImageCount / self.IMAGE_COUNT_PER_PAGE > pageCount - 1:
                    pageCount += 1
                else:
                    # ȫ��ͼƬ�������
                    break
            
            if newMemberUidList[userId][2]!=0 and (imageCount * 2) > int(newMemberUidList[userId][2]):
                isError = True
            
            self.printStepMsg(userName + "������ϣ��ܹ����" + str(imageCount - 1) + "��ͼƬ")
            newMemberUidList[userId][2] = str(int(newMemberUidList[userId][2]) + imageCount - 1)
            allImageCount += imageCount - 1
            
            # ����
            if self.isSort == 1:
                imageList = sorted(os.listdir(imagePath), reverse=True)
                # �ж�����Ŀ���ļ����Ƿ����
                if len(imageList) >= 1:
                    destPath = self.imageDownloadPath + "\\" + userName
                    if os.path.exists(destPath):
                        if os.path.isdir(destPath):
                            self.printStepMsg("ͼƬ����Ŀ¼: " + destPath + " �Ѵ��ڣ�ɾ����")
                            self.removeDirFiles(destPath)
                        else:
                            self.printStepMsg("ͼƬ����Ŀ¼: " + destPath + "�Ѵ�����ͬ���ֵ��ļ����Զ�ɾ��")
                            os.remove(destPath)
                    # self.printStepMsg("create image download path: " + destPath)
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
        tmpList = []
        tmpUserIdList = sorted(newMemberUidList.keys())
        for index in tmpUserIdList:
            tmpList.append("\t".join(newMemberUidList[index]))
        newMemberUidListString = "\n".join(tmpList)
        newMemberUidListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.memberUIdListFilePath)[-1]
        self.printStepMsg("save new id list file: " + newMemberUidListFilePath)
        newMemberUidListFile = open(newMemberUidListFilePath, 'w')
        newMemberUidListFile.write(newMemberUidListString)
        newMemberUidListFile.close()
        
        stopTime = time.time()
        self.printStepMsg("�浵�ļ��������û�ͼƬ�ѳɹ����أ���ʱ" + str(int(stopTime - startTime)) + "�룬����ͼƬ" + str(allImageCount) + "��")

if __name__ == '__main__':
    weibo().main()
