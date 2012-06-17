#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtCore, QtGui

#**************************************************************************************************
# class: ClickableLabel
#**************************************************************************************************

class ClickableLabel(QtGui.QLabel):
    __data = None
    clicked = QtCore.Signal()

    def data(self):
        return self.__data

    def setData(self, data):
        self.__data = data

    def mouseReleaseEvent(self, *args, **kwargs):
        self.clicked.emit()

