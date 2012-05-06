#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

import sys
from PySide import QtCore, QtGui
from MainWindow import MainWindow

app = QtGui.QApplication(sys.argv)
QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName('UTF-8'))
mainWindows = MainWindow()
mainWindows.show()
sys.exit(app.exec_())


