# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

import xmlrpclib
from PySide import QtCore

#**************************************************************************************************
# class: SynchronizationThread
#**************************************************************************************************

class SynchronizationThread(QtCore.QThread):
    """
    Поток синхронизации с сервером
    """

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.__server = None
        self.__response = None

    def _response(self):
        return self.__response

    def _setHostName(self, hostname):
        self.__server = xmlrpclib.ServerProxy(hostname)

    def run(self, *args, **kwargs):
        try:
            self.__response = None
            self.__response = self.__server.server.check()
        except Exception:
            pass
