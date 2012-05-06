#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore

#**************************************************************************************************
# class: Answer
# data:
#   document (object) - Текст ответа
#   right (bool) - Правильный либо неправильный ответ
#**************************************************************************************************

class Answer(QtCore.QObject):
    def __init__(self, document='', right=False):
        QtCore.QObject.__init__(self)
        self.__document = document
        self.__right = right

    changed = QtCore.Signal()

    # Methods get and set (START)
    def _document(self): return self.__document

    def _right(self): return self.__right

    def _setDocument(self, document):
        self.__document = document
        self.changed.emit()

    def _setRight(self, right):
        self.__right = right
        self.changed.emit()

        # Methods get and set (END)

    document = QtCore.Property(object, _document, _setDocument, notify=changed)
    right = QtCore.Property(bool, _right, _setRight, notify=changed)