# -*- coding:utf-8  -*-
'''
Created on 2013-4-8

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
如有问题或建议请联系
'''

from common import common
import copy
import os
import shutil
import time

class downloadImage(common.Tool):
    
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
        # 配置文件获取日志文件路径
        self.errorLogPath = self.getConfig(config, "ERROR_LOG_FILE_NAME", "\\log\\errorLog.txt", 3)
        self.traceLogPath = self.getConfig(config, "TRACE_LOG_FILE_NAME", "\\log\\traceLog.txt", 3)
        self.stepLogPath = self.getConfig(config, "STEP_LOG_FILE_NAME", "\\log\\stepLog.txt", 3)
        self.imageDownloadPath = self.getConfig(config, "IMAGE_DOWNLOAD_DIR_NAME", "\\photo", 3)
        self.imageTempPath = self.getConfig(config, "IMAGE_TEMP_DIR_NAME", "\\tempImage", 3)
        self.memberUIdListFilePath = self.getConfig(config, "MEMBER_UID_LIST_FILE_NAME", "\\info\\idlist.txt", 3)
        # 配置文件获取程序配置
        self.isLog = self.getConfig(config, "IS_LOG", 1, 2)
        self.isShowError = self.getConfig(config, "IS_SHOW_ERROR", 1, 2)
        self.isDebug = self.getConfig(config, "IS_DEBUG", 1, 2)
        self.isShowStep = self.getConfig(config, "IS_SHOW_STEP", 1, 2)
        self.isSort = self.getConfig(config, "IS_SORT", 1, 2)
        self.getImageCount = self.getConfig(config, "GET_IMAGE_COUNT", 1, 2)
        self.isProxy = self.getConfig(config, "IS_PROXY", 2, 2)
        self.proxyIp = self.getConfig(config, "PROXY_IP", "127.0.0.1", 0)
        self.proxyPort = self.getConfig(config, "PROXY_PORT", "8087", 0)
        self.printMsg(u"配置文件读取完成")

    def main(self):
        startTime = time.time()
        # 判断各种目录是否存在
        # 日志文件保存目录
        if self.isLog == 1:
            stepLogDir = os.path.dirname(self.stepLogPath)
            if not os.path.exists(stepLogDir):
                if not self.createDir(stepLogDir):
                    self.printErrorMsg(u"创建步骤日志目录：" + stepLogDir + u" 失败，程序结束！", self.isShowError, self.isLog)
                    self.processExit()
                self.printStepMsg(u"步骤日志目录不存在，创建文件夹: " + stepLogDir, self.isShowError, self.isLog)
            errorLogDir = os.path.dirname(self.errorLogPath)
            if not os.path.exists(errorLogDir):
                if not self.createDir(errorLogDir):
                    self.printErrorMsg(u"创建错误日志目录：" + errorLogDir + u" 失败，程序结束！", self.isShowError, self.isLog)
                    self.processExit()
                self.printStepMsg(u"错误日志目录不存在，创建文件夹: " + errorLogDir, self.isShowError, self.isLog)
            traceLogDir = os.path.dirname(self.traceLogPath)
            if not os.path.exists(traceLogDir):
                if not self.createDir(traceLogDir):
                    self.printErrorMsg(u"创建调试日志目录：" + traceLogDir + u" 失败，程序结束！", self.isShowError, self.isLog)
                    self.processExit()
                self.printStepMsg(u"调试日志目录不存在，创建文件夹: " + traceLogDir, self.isShowError, self.isLog)
        # 图片下载目录
        if os.path.exists(self.imageDownloadPath):
            if os.path.isdir(self.imageDownloadPath):
                isDelete = False
                while not isDelete:
                    # 手动输入是否删除旧文件夹中的目录
                    input = raw_input(u"图片下载目录：" + self.imageDownloadPath + u" 已经存在，是否需要删除该文件夹并继续程序？(Y)es or (N)o: ")
                    try:
                        input = input.lower()
                        if input in ["y", "yes"]:
                            isDelete = True
                        elif input in ["n", "no"]:
                            self.processExit()
                    except Exception, e:
                        self.printErrorMsg(str(e), self.isShowError, self.isLog) 
                        pass
                self.printStepMsg(u"删除图片下载目录: " + self.imageDownloadPath, self.isShowError, self.isLog)
                # 删除目录
                shutil.rmtree(self.imageDownloadPath, True)
                # 保护，防止文件过多删除时间过长，5秒检查一次文件夹是否已经删除
                while os.path.exists(self.imageDownloadPath):
                    time.sleep(5)
            else:
                self.printStepMsg(u"图片下载目录: " + self.imageDownloadPath + u"已存在相同名字的文件，自动删除", self.isShowError, self.isLog)
                os.remove(self.imageDownloadPath)
        self.printStepMsg(u"创建图片下载目录: " + self.imageDownloadPath, self.isShowError, self.isLog)
        if not self.createDir(self.imageDownloadPath):
            self.printErrorMsg(u"创建图片下载目录：" + self.imageDownloadPath + u" 失败，程序结束！", self.isShowError, self.isLog)
            self.processExit()
        # 设置代理
        if self.isProxy == 1 or self.isProxy == 2:
            self.proxy(self.proxyIp, self.proxyPort, "https")
        # 寻找idlist，如果没有结束进程
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
            self.printErrorMsg(u"用户ID存档文件: " + self.memberUIdListFilePath + u"不存在，程序结束！", self.isShowError, self.isLog)
            self.processExit()
        # 创建临时存档文件
        newMemberUidListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.memberUIdListFilePath)[-1]
        newMemberUidListFile = open(newMemberUidListFilePath, 'w')
        newMemberUidListFile.close()
        # 复制处理存档文件
        newMemberUidList = copy.deepcopy(userIdList)
        for newUserId in newMemberUidList:
            # 如果没有名字，则名字用uid代替
            if len(newMemberUidList[newUserId]) < 2:
                newMemberUidList[newUserId].append(newMemberUidList[newUserId][0])
            # 如果没有出事image count，则为0
            if len(newMemberUidList[newUserId]) < 3:
                newMemberUidList[newUserId].append("0")
            # 处理上一次image URL
            # 需置空存放本次第一张获取的image URL
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
            # 处理member 队伍信息
            if len(newMemberUidList[newUserId]) < 7:
                newMemberUidList[newUserId].append("")
        
        allImageCount = 0
        # 循环下载每个id
        for userId in sorted(userIdList.keys()):
            userName = newMemberUidList[userId][1]
            self.printStepMsg(u"UID: " + str(userId) + u", 名字: " + userName.decode("GBK"), self.isShowError, self.isLog)
            # 初始化数据
            pageCount = 0
            imageCount = 1
            messageUrlList = []
            imageUrlList = []
            isPass = False
            # 如果有存档记录，则直到找到与前一次一致的地址，否则都算有异常
            if len(userIdList[userId]) > 3 and userIdList[userId][3].find("picasaweb.google.com/") != -1 and int(userIdList[userId][2]) != 0:
                isError = True
            else:
                isError = False
            # 如果需要重新排序则使用临时文件夹，否则直接下载到目标目录
            if self.isSort == 1:
                imagePath = self.imageTempPath
            else:
                imagePath = self.imageDownloadPath + "\\" + userName
            if not self.createDir(imagePath):
                self.printErrorMsg(u"创建图片下载目录： " + imagePath + u" 失败，程序结束！", self.isShowError, self.isLog)
                self.processExit()
            # 图片下载  
            while 1:
                if isPass:
                    break
                # 获取信息总页,offset=N表示返回最新的N到N+100条信息所在的url
                photoAlbumUrl = "https://plus.google.com/_/photos/posts/%s?offset=%s" % (userId, pageCount)
                self.trace(u"相册专辑地址：" + photoAlbumUrl, self.isShowError, self.isLog)
                photoAlbumPage = self.doGet(photoAlbumUrl)
                if not photoAlbumPage:
                    self.printErrorMsg(u"无法获取相册首页: " + photoAlbumUrl, self.isShowError, self.isLog)
                    isPass = True
                    break
            
                # 判断信息总页字节数大小，是否小于300（下载到最后一页），结束
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
                    # 将第一张image的URL保存到新id list中
                    if newMemberUidList[userId][3] == "":
                        newMemberUidList[userId][3] = messageUrl
                    # 检查是否已下载到前一次的图片
                    if len(userIdList[userId]) >= 4 and userIdList[userId][3].find("picasaweb.google.com/") != -1:
                        if messageUrl == userIdList[userId][3]:
                            isPass = True
                            isError = False
                            break
                    self.trace(u"message URL:" + messageUrl, self.isShowError, self.isLog)
                    # 判断是否重复
                    if messageUrl in messageUrlList:
                        messageIndex += 1
                        continue
                    messageUrlList.append(messageUrl)
                    messagePage = self.doGet(messageUrl)
                    if not messagePage:
                        # self.printErrorMsg("can not get messagePage: " + messageUrl, self.isShowError, self.isLog)
                        self.printErrorMsg(u"无法获取信息页: " + messageUrl, self.isShowError, self.isLog)
                        messageIndex += 1
                        continue
                    flag = messagePage.find("<div><a href=")
                    while flag != -1:
                        imageIndex = messagePage.find("<img src=", flag, flag + 200)
                        if imageIndex == -1:
                            self.printErrorMsg(u"信息页：" + messageUrl + u" 中没有找到标签'<img src='", self.isShowError, self.isLog)
                            break
                        imageStart = messagePage.find("http", imageIndex)
                        imageStop = messagePage.find('"', imageStart)
                        imageUrl = messagePage[imageStart:imageStop]
                        self.trace(u"image URL:" + imageUrl, self.isShowError, self.isLog)
                        if imageUrl in imageUrlList:
                            flag = messagePage.find("<div><a href=", flag + 1)
                            continue
                        tempList = imageUrl.split("/")
                        # 使用最大分辨率
                        tempList[-2] = "s0"
                        imageUrl = "/".join(tempList)
                        # 文件类型
                        fileType = imageUrl.split(".")[-1]
                        imgByte = self.doGet(imageUrl)
                        if imgByte:
                            # 保存图片
                            filename = str("%04d" % imageCount)
                            imageFile = open(imagePath + "\\" + str(filename) + "." + fileType, "wb")
                            self.printStepMsg(u"开始下载第" + str(imageCount) + u"张图片：" + imageUrl, self.isShowError, self.isLog)
                            imageFile.write(imgByte)
                            imageFile.close()
                            self.printStepMsg(u"下载成功", self.isShowError, self.isLog)
                            imageCount += 1
                            # 达到配置文件中的下载数量，结束
                            if self.getImageCount > 0 and imageCount > self.getImageCount:
                                isPass = True
                                break
                        else:
                            self.printErrorMsg(u"获取图片信息失败：" + str(userId) + ": " + imageUrl, self.isShowError, self.isLog)
                        flag = messagePage.find("<div><a href=", flag + 1)
                    messageIndex += 1
                pageCount += 100
                
            self.printStepMsg(userName.decode("GBK") + u"下载完毕，总共获得" + str(imageCount - 1) + u"张图片", self.isShowError, self.isLog)
            # 检查下载图片是否大于总数量的一半，对上一次记录的图片正好被删除或其他原因导致下载了全部图片做一个保护
            newMemberUidList[userId][2] = str(int(newMemberUidList[userId][2]) + imageCount - 1)
            allImageCount += imageCount - 1
            
            # 排序
            if self.isSort == 1:
                imageList = sorted(os.listdir(imagePath), reverse=True)
                # 判断排序目标文件夹是否存在
                if len(imageList) >= 1:
                    destPath = self.imageDownloadPath + "\\" + newMemberUidList[userId][6] + "\\" + userName
                    if os.path.exists(destPath):
                        if os.path.isdir(destPath):
                            self.printStepMsg("图片保存目录: " + destPath + " 已存在，删除中", self.isShowError, self.isLog)
                            self.removeDirFiles(destPath)
                        else:
                            self.printStepMsg("图片保存目录: " + destPath + "已存在相同名字的文件，自动删除中", self.isShowError, self.isLog)
                            os.remove(destPath)
                    self.printStepMsg("创建图片保存目录: " + destPath, self.isShowError, self.isLog)
                    if not self.createDir(destPath):
                        self.printErrorMsg("创建图片保存目录： " + destPath + " 失败，程序结束！", self.isShowError, self.isLog)
                        self.processExit()
                    # 倒叙排列
                    if len(userIdList[userId]) >= 3:
                        count = int(userIdList[userId][2]) + 1
                    else:
                        count = 1
                    for fileName in imageList:
                        fileType = fileName.split(".")[1]
                        shutil.copyfile(imagePath + "\\" + fileName, destPath + "\\" + str("%04d" % count) + "." + fileType)
                        count += 1
                    self.printStepMsg("图片从下载目录移动到保存目录成功", self.isShowError, self.isLog)
                # 删除临时文件夹
                shutil.rmtree(imagePath, True)

            if isError:
                self.printErrorMsg(userName.decode("GBK") + "图片数量异常，请手动检查", self.isShowError, self.isLog)

            # 保存最后的信息
            newMemberUidListFile = open(newMemberUidListFilePath, 'a')
            newMemberUidListFile.write("\t".join(newMemberUidList[userId]) + "\n")
            newMemberUidListFile.close()

        # 排序并保存新的idList.txt
        tempList = []
        tempUserIdList = sorted(newMemberUidList.keys())
        for index in tempUserIdList:
            tempList.append("\t".join(newMemberUidList[index]))
        newMemberUidListString = "\n".join(tempList)
        newMemberUidListFilePath = os.getcwd() + "\\info\\" + time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time())) + os.path.split(self.memberUIdListFilePath)[-1]
        self.printStepMsg("保存新存档文件：" + newMemberUidListFilePath, self.isShowError, self.isLog)
        newMemberUidListFile = open(newMemberUidListFilePath, 'w')
        newMemberUidListFile.write(newMemberUidListString)
        newMemberUidListFile.close()
        
        stopTime = time.time()
        self.printStepMsg("存档文件中所有用户图片已成功下载，耗时" + str(int(stopTime - startTime)) + "秒，共计图片" + str(allImageCount) + "张", self.isShowError, self.isLog)

if __name__ == '__main__':
    downloadImage().main()
