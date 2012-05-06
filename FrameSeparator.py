#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtGui

#**************************************************************************************************
# class: FrameSeparator
#**************************************************************************************************

class FrameSeparator(QtGui.QFrame):
    """
    Разделитель
    """

    def __init__(self, shape, shadow):
        QtGui.QFrame.__init__(self)

        self.setFrameShape(shape)
        self.setFrameShadow(shadow)