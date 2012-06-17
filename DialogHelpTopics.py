# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtGui, QtWebKit

#**************************************************************************************************
# class: DialogHelpTopics
#**************************************************************************************************

class DialogHelpTopics(QtGui.QDialog):
    """
    Диалоговое окно справки
    """

    def __init__(self, title, url):
        QtGui.QDialog.__init__(self)
        # WebView
        self.__webView = QtWebKit.QWebView()
        self.__webView.load(url)
        self.show()
        # Layout
        self.__layoutVMain = QtGui.QVBoxLayout()
        self.__layoutVMain.addWidget(self.__webView)
        # <<<Self>>>
        self.setLayout(self.__layoutVMain)
        self.setModal(True)
        self.setWindowTitle(title)
        #self.resize(350, 200)
