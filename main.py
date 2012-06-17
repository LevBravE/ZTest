#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

import sys
from PySide import QtCore, QtGui
from MainWindow import MainWindow

def readStyleSheet(app, fileName):
    """
    Загрузить файл стилей приложения
    """
    file = QtCore.QFile(fileName)
    if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
        return False
    app.setStyleSheet(str(file.readAll()))
    return True

app = QtGui.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('img/ztestlogo40x40.png'))

readStyleSheet(app, 'qss/style.qss')
translator = QtCore.QTranslator()
if translator.load('qt_ru', 'translations'):
    app.installTranslator(translator)

QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
mainWindows = MainWindow()
mainWindows.show()
sys.exit(app.exec_())


