#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

import random
from PySide import QtCore, QtGui
from ImgParser import ImgParser

#**************************************************************************************************
# class: TextEditInsertImage
#**************************************************************************************************

class TextEditInsertImage(QtGui.QTextEdit):
    """
    TextEdit со возможностью добавления картинок из
    буфера (Совместим с MSWord)
    """

    def __init__(self):
        QtGui.QTextEdit.__init__(self)

    def _addResource(self, fileName, imageName):
        image = QtGui.QImageReader(fileName)
        # ресурс добавляется в хранилище ресурсов документа
        self.document().addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(imageName), image.read())

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        # вставка картинки
        if source.hasImage():
            # принятые данные преобразуются в тип QImage
            image = source.imageData()
            # генерируется имя ресурса
            image_name = 'image%s' % random.random()
            # ресурс добавляется в хранилище ресурсов документа
            self.document().addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(image_name), image)
            # картинка вставляется в текст
            cursor.insertImage(image_name)
        elif source.hasHtml and source.html():
            imgParser = ImgParser(source.html())

            for itemImg in imgParser._listImagePath():
                # itemImg[0] - path, itemImg[1] - image name
                self._addResource(itemImg[0], itemImg[1])
            cursor.insertHtml(imgParser._text())
        elif source.hasText:
            text = source.text()
            cursor.insertText(text)

