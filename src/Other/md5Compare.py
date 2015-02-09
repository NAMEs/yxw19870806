# -*- coding:GBK  -*-
'''
Created on 2013-4-8

@author: hikaru
QQ: 286484545
email: hikaru870806@hotmail.com
���������������ϵ
'''

import hashlib
import os
import shutil
import time

class md5Compare():
    
    # ����Ŀ¼��ȫ���ļ���md5��
    def _scanPath(self, rootDir, sourceDir, result):
        for file in os.listdir(sourceDir):
            sourceFile = os.path.join(sourceDir, file)
            if os.path.isfile(sourceFile):
                md5Result = self._md5(sourceFile)
                result[sourceFile.replace(rootDir, '')] = md5Result
            if os.path.isdir(sourceFile):
                self._scanPath(rootDir, sourceFile, result)
    
    def _md5(self, sourceFile):
        print 'start md5: ' + sourceFile
        file = open(sourceFile, 'rb')
        pos = 0  
        buff = 1024 * 1024 * 256 # ��ȡ256MB
        hash = hashlib.md5()
        while 1:
            file.seek(pos)  
            buffByte = file.read(buff) #���ļ��ж�ȡһ������  
            if not buffByte:  
                break;
            hash.update(buffByte)
            pos += buff #����ȡ��һ�����ݳ���  
            time.sleep(0.1)
        return str(hash.hexdigest())
    
    def createMd5Result(self, sourcePath):
        result = {}
        self._scanPath(sourcePath, sourcePath, result)
        return result

    def readMd5ResultFile(self, md5ResultfilePath):
        result = {}
        md5Resultfile = open(md5ResultfilePath, 'r')
        lines = md5Resultfile.readlines()
        for line in lines:
            temp = line.replace('\n', '').split('\t')
            result[temp[0]] = temp[1]
        return result

    def writeMd5ResultFIle(self, md5ResultfilePath, result):
        if result:
            md5Resultfile = open(md5ResultfilePath, 'w')
            for i in result:
                md5Resultfile.write(i + '\t' + result[i] + '\n')
            md5Resultfile.close()

if __name__ == "__main__":
    gamePath = 'D:\Steam\steamapps\common\Warframe' # �ȶ�Ŀ¼
    md5ResultfilePath = 'md5.txt' # md5��¼�ļ�·��
    copyDestPath = 'D:\\WF' # �����ļ����Ƴ�����Ŀ¼
    different = []
    # ĿǰĿ¼�µ������ļ�MD5��
    newResult = md5Compare().createMd5Result(gamePath)
    # �ϴαȶԲ�����MD5���¼
    oldResult = md5Compare().readMd5ResultFile(md5ResultfilePath)
    for i in newResult:
        # ���ļ�����
        if oldResult.has_key(i):
            # md5ֵ����ͬ
            if newResult[i] != oldResult[i]:
                different.append(i)
        # ���ļ�
        else:
            different.append(i)
    print 'different count: ' + str(len(different))
    
    # д�µ�md5��
    md5Compare().writeMd5ResultFIle(md5ResultfilePath, newResult)
    
#    for file in different:
#        sourceFile = gamePath + file
#        destFile = copyDestPath + file
#        destDir = os.path.dirname(destFile)
#        if not os.path.exists(destDir):
#            os.makedirs(destDir)
#        shutil.copyfile(sourceFile, destFile)
        