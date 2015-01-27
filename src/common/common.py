# -*- coding:GBK  -*-
'''
Created on 2013-7-16

@author: Administrator
'''

IS_SET_TIMEOUT = False

class Tool(object):

    def doGet(self, url, postData=None):
    # http����
        import sys
        import time
        import traceback
        import urllib2
        global IS_SET_TIMEOUT
        if url.find("http") == -1:
            return None
        count = 0
        while 1:
            try:
                if postData:
                    request = urllib2.Request(url, postData)
                else:
                    request = urllib2.Request(url)
                # ����ͷ��Ϣ
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 FirePHP/0.7.2')
                # ���÷��ʳ�ʱ
                if sys.version_info < (2, 7):
                    if not IS_SET_TIMEOUT:
                        urllib2.socket.setdefaulttimeout(5)
                        IS_SET_TIMEOUT = True
                    response = urllib2.urlopen(request)
                else:
                    response = urllib2.urlopen(request, timeout=5)
                return response.read()
            except Exception, e:
                # �����޷�����
                if str(e).find("[Errno 10061]") != -1:
                    input = raw_input("�޷����ʴ��������������������á��Ƿ���Ҫ��������(Y)es or (N)o��").lower()
                    if input in ["y", "yes"]:
                        pass
                    elif input in ["n", "no"]:
                        sys.exit()
                # ���ӱ��رգ��ȴ�1���Ӻ��ٳ���
                elif str(e).find("[Errno 10053] ") != -1:
                    self.printMsg("����ҳ�泬ʱ�������������Ժ�")
                    time.sleep(60)
                # ��ʱ
                elif str(e).find("timed out") != -1:
                    self.printMsg("����ҳ�泬ʱ�������������Ժ�")
                else:
                    self.printMsg(str(e))
                    traceback.print_exc()
            count += 1
            if count > 50:
                self.printErrorMsg("�޷�����ҳ�棺" + url)
                return False

    def getDefaultBrowserCookiePath(self, OSVersion, browserType):     
    # ����������Ͳ���ϵͳ���Զ�����Ĭ�������cookie·��
    # OSVersion=1: win7
    # OSVersion=2: xp
    # browserType=1: IE
    # browserType=2: firefox
    # browserType=3: chrome
        import getpass
        import os
        if browserType == 1:
            if OSVersion == 1:
                return "C:\\Users\\%s\\AppData\\Roaming\\Microsoft\\Windows\\Cookies\\" % (getpass.getuser())
            elif OSVersion == 2:
                return "C:\\Documents and Settings\\%s\\Cookies\\" % (getpass.getuser())
        elif browserType == 2:
            if OSVersion == 1:
                defaultBrowserPath = "C:\\Users\\%s\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\" % (getpass.getuser())
                for dirName in os.listdir(defaultBrowserPath):
                    if os.path.isdir(defaultBrowserPath + "\\" + dirName):
                        if os.path.exists(defaultBrowserPath + "\\" + dirName + "\\cookies.sqlite"):
                            return defaultBrowserPath + "\\" + dirName + "\\"
            elif OSVersion == 2:
                defaultBrowserPath = "C:\\Documents and Settings\\%s\\Local Settings\\Application Data\\Mozilla\\Firefox\\Profiles\\" % (getpass.getuser())
                for dirName in os.listdir(defaultBrowserPath):
                    if os.path.isdir(defaultBrowserPath + "\\" + dirName):
                        if os.path.exists(defaultBrowserPath + "\\" + dirName + "\\cookies.sqlite"):
                            return defaultBrowserPath + "\\" + dirName + "\\"                
        elif browserType == 3:
            if OSVersion == 1:
                return "C:\\Users\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default" % (getpass.getuser())
            elif OSVersion == 2:
                return "C:\\Documents and Settings\\%s\\Local Settings\\Application Data\\Google\\Chrome\\User Data\Default\\" % (getpass.getuser())
        elif browserType == 4:
            if OSVersion == 1:
                return "C:\\Users\\%s\\AppData\\Local\\MapleStudio\\ChromePlus\\User Data\\Default\\" % (getpass.getuser())
            elif OSVersion == 2:
                return "C:\\Documents and Settings\\%s\\Local Settings\\Application Data\\MapleStudio\\ChromePlus\\User Data\\Default\\" % (getpass.getuser())
        self.printMsg("��������ͣ�" + browserType + "������")
        return None

    def cookie(self, filePath, browserType=1):
    # ʹ��ϵͳcookies
    # browserType=1: IE
    # browserType=2: firefox
    # browserType=3: chrome
        import cookielib
        import cStringIO
        import os
        import urllib2
        from pysqlite2 import dbapi2 as sqlite
        if not os.path.exists(filePath):
            self.printMsg("cookieĿ¼��" + filePath + " ������")
            return False
        ftstr = ["FALSE", "TRUE"]
        s = cStringIO.StringIO()
        s.write("# Netscape HTTP Cookie File\n")
        if browserType == 1:
            for cookieName in os.listdir(filePath):
                if cookieName.find(".txt") == -1:
                    continue
                cookieFile = open(filePath + "\\" + cookieName, 'r')
                cookieInfo = cookieFile.read()
                cookieFile.close()
                for cookies in cookieInfo.split("*"):
                    cookieList = cookies.strip("\n").split("\n")
                    if len(cookieList) >= 8:
                        domain = cookieList[2].split("/")[0]
                        domainSpecified = ftstr[cookieList[2].startswith('.')]
                        path = cookieList[2].replace(domain, "")
                        secure = ftstr[0]
                        expires = cookieList[4]
                        name = cookieList[0]
                        value = cookieList[1]
                        s.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (domain, domainSpecified, path, secure, expires, name, value))
        elif browserType == 2:
            con = sqlite.connect(filePath + "\\cookies.sqlite")
            cur = con.cursor()
            cur.execute("select host, path, isSecure, expiry, name, value from moz_cookies")
            for cookieInfo in cur.fetchall():
                domain = cookieInfo[0]
                domainSpecified = ftstr[cookieInfo[0].startswith('.')]
                path = cookieInfo[1]
                secure = ftstr[cookieInfo[2]]
                expires = cookieInfo[3]
                name = cookieInfo[4]
                value = cookieInfo[5]
#                 s.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (domain, domainSpecified, path, secure, expires, name, value))
                try:
                    s.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (domain, domainSpecified, path, secure, expires, name, value))
                except:
                    pass
        elif browserType in [3, 4]:
            con = sqlite.connect(filePath + "\\Cookies")
            cur = con.cursor()
            cur.execute("select host_key, path, secure, expires_utc, name, value from cookies")
            for cookieInfo in cur.fetchall():
                domain = cookieInfo[0]
                domainSpecified = ftstr[cookieInfo[0].startswith('.')]
                path = cookieInfo[1]
                secure = ftstr[cookieInfo[2]]
                expires = cookieInfo[3]
                name = cookieInfo[4]
                value = cookieInfo[5]
                s.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (domain, domainSpecified, path, secure, expires, name, value))
        s.seek(0)
        cookieJar = cookielib.MozillaCookieJar()
        cookieJar._really_load(s, '', True, True)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        urllib2.install_opener(opener)
        return True
    
    def proxy(self, ip, port, protocol):
    # ���ô���
        import urllib2
        proxyHandler = urllib2.ProxyHandler({protocol:"http://" + ip + ":" + port})
        opener = urllib2.build_opener(proxyHandler)
        urllib2.install_opener(opener)
        self.printMsg("���ô���ɹ�")
                
    def getConfig(self, config, key, defaultValue, mode, prefix=None, postfix=None):
    # ��ȡ�����ļ�
    # config : �ֵ��ʽ���磺{key1:value1, key2:value2}
    # mode 0 : ֱ�Ӹ�ֵ
    # mode 1 : �ַ���ƴ��
    # mode 2 : ȡ��
    # mode 3 : �ļ�·������'\'��ͷ��Ϊ��ǰĿ¼�´���
    # prefix: ǰ׺��ֻ����mode=1ʱ��Ч
    # postfix: ��׺��ֻ����mode=1ʱ��Ч
        import os
        import traceback
        value = None
        if config.has_key(key):
            if mode == 0:
                value = config[key]
            elif mode == 1:
                value = config[key]
                if prefix != None:
                    value = prefix + value
                if postfix != None:
                    value = value + postfix
            elif mode == 2:
                try:
                    value = int(config[key])
                except:
                    self.printMsg("�����ļ�config.ini��keyΪ'" + key + "'��ֵ������һ��������ʹ�ó���Ĭ������")
                    traceback.print_exc()
                    value = defaultValue
            elif mode == 3:
                value = config[key]
                if value[0] == "\\":
                    value = os.getcwd() + value
                return value
        else:
            self.printMsg("�����ļ�config.ini��û���ҵ�keyΪ'" + key + "'�Ĳ�����ʹ�ó���Ĭ������")
            value = defaultValue
        return value
    
    def printMsg(self, msg, isTime=True):
        if isTime:
            msg = self.getTime() + " " + msg
        print msg
    
    def trace(self, msg, isPrint=1, logPath=''):
        if isPrint == 1:
            msg = self.getTime() + " " + msg
#             self.printMsg(msg, False)
        if logPath != '':
            self.writeFile(msg, logPath)
    
    def printErrorMsg(self, msg, isPrint=1, logPath=''):
        if isPrint == 1:
            msg = self.getTime() + " [Error] " + msg
            self.printMsg(msg, False)
        if logPath != '':
            if msg.find("HTTP Error 500") != -1:
                return
            if msg.find("urlopen error The read operation timed out") != -1:
                return
            self.writeFile(msg, logPath)
    
    def printStepMsg(self, msg, isPrint=1, logPath=''):
        if isPrint == 1:
            msg = self.getTime() + " " + msg
            self.printMsg(msg, False)
        if logPath != '':
            self.writeFile(msg, logPath)
                
    def getTime(self):
        import time
        return time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
    
    def writeFile(self, msg, filePath):
        logFile = open(filePath, 'a')
        logFile.write(msg + "\n")
        logFile.close()
    
    def createDir(self, path):
        import time
        import traceback
        import os
        if not os.path.exists(path):
            count = 0
            while 1:
                try:
                    if count >= 5:
                        return False
                    os.makedirs(path)
                    if os.path.isdir(path):
                        return True
                except Exception, e:
                    self.printMsg(str(e))
                    traceback.print_exc()
                    time.sleep(5)
                count += 1
        return True
    
    def removeDirFiles(self, dirPath): 
        import os
        for fileName in os.listdir(dirPath): 
            targetFile = os.path.join(dirPath, fileName) 
            if os.path.isfile(targetFile): 
                os.remove(targetFile)
                
    def processExit(self):
        import sys
        sys.exit()
    
