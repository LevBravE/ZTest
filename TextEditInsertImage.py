#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

import random
from PySide import QtCore, QtGui
from HtmlContent import HtmlContent

#**************************************************************************************************
# class: TextEditInsertImage
#**************************************************************************************************

class TextEditInsertImage(QtGui.QTextEdit):
    """
    TextEdit со возможностью добавления картинок из
    буфера
    """

    def __init__(self):
        QtGui.QTextEdit.__init__(self)

    def addResource(self):
        print 'addResource'

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        document = self.document()
        htmlContent = HtmlContent()

        print source.html()

        # вставка картинки
        if source.hasImage() and False:
            # принятые данные преобразуются в тип QImage
            image = source.imageData()
            print image
            # генерируется имя ресурса
            image_name = 'image%s' % random.random()
            # ресурс добавляется в хранилище ресурсов документа
            document.addResource(QtGui.QTextDocument.ImageResource, QtCore.QUrl(image_name), image)
            # картинка вставляется в текст
            cursor.insertImage(image_name)
            print 'image'

        if source.hasHtml:
            htmlContent.feed(source.html())
            #html = htmlContent._contentNotImg()
            #print source.html()
            #cursor.insertHtml(source.html())
        if source.hasText:
            text = source.text()
            #cursor.insertText(text)
            #print 'text'

        QtGui.QTextEdit.insertFromMimeData(self, source)

