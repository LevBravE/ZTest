#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

import re, random

#**************************************************************************************************
# class: ImgParser
#**************************************************************************************************

class ImgParser(object):
    def __init__(self, text):
        object.__init__(self)
        self.__text = text
        self.__lstPath = []
        # <img ... >
        self.__regImg = re.compile('(<img.*[^>]+.)')
        # C:\ ... or / ... (Windows or Unix)
        self.__regPath = re.compile('(?<=src="file:///)[^ \f\n\r\t\v\"]+')
        self.__lstImg = self.__regImg.findall(self.__text)

    def _text(self):
        return self.__text

    def _listImagePath(self):
        for imgIndex, imgItem in enumerate(self.__lstImg):
            try:
                strPath = self.__regPath.findall(imgItem)[0]
                # генерируется имя ресурса
                imageName = 'image%s' % random.random()
                self.__lstPath.append([])
                self.__lstPath[imgIndex].append(strPath)
                self.__lstPath[imgIndex].append(imageName)
                # замена тега img
                regWidth = re.search('(?<=width=)\d+', imgItem)
                regHeight = re.search('(?<=height=)\d+', imgItem)
                strNewImg = '<img width=%s height=%s src="%s">' % (regWidth.group(0), regHeight.group(0), imageName)
                self.__text = self.__text.replace(imgItem, strNewImg)
            except IndexError:
                pass

        return self.__lstPath

