# -*- coding:GBK  -*-
'''
Created on 2013-4-14

@author: hikaru

���Ŀ¼��txt�ļ���ͼƬ������һ�µĳ�Ա����
'''

import os

def getCount(idPath, imageRootPath):
    tempFile = open(idPath, 'r')
    lines = tempFile.readlines()
    tempFile.close()
    for line in lines:
        line = line.split("\t")
        imagePath = imageRootPath + line[1]
        if os.path.exists(imagePath):
            count1 = len(os.listdir(imagePath))
        else:
            count1 = 0
        count2 = int(line[2])
        if count1 != count2:
            print line[1] + ": " + str(count1) + ", " + str(count2)
    print "check over!"

getCount("info\\idlist_2.txt", "Z:\\G+\\weibo2\\")
getCount("info\\idlist.txt", "Z:\\G+\\weibo\\")
