# -*- coding:GBK  -*-
'''
Created on 2013-4-14

@author: hikaru

���Ŀ¼��txt�ļ���ͼƬ������һ�µĳ�Ա����
'''

import os

imageRootPath = "Z:\\G+\\photo\\"

def getCount(path):
    tempFile = open(path, 'r')
    lines = tempFile.readlines()
    tempFile.close()
    for line in lines:
        line = line.split("\t")
        imagePath = imageRootPath + line[6].replace("\n", "") + "\\" + line[1]
        count1 = len(os.listdir(imagePath))
        count2 = int(line[2])
        if count1 != count2:
            print line[1] + ": " + str(count1) + ", " + str(count2)
    print "check over!"

getCount("info\\idlist.txt")
