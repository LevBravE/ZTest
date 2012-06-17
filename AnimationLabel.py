# -*- coding: utf-8 -*-

__author__ = 'LevBravE'

from PySide import QtGui

#**************************************************************************************************
# class: AnimationLabel
#**************************************************************************************************

class AnimationLabel(QtGui.QLabel):
    def __init__(self, animationPath, size=None):
        QtGui.QLabel.__init__(self)
        self.__animationPath = animationPath
        self.__size = size
        # Movie
        self.__animationMovie = QtGui.QMovie(self.__animationPath)
        # <<<Self>>>
        self.setHidden(True)
        if self.__size:
            self.setFixedSize(self.__size)
        self.setMovie(self.__animationMovie)

    def _start(self):
        if self.__animationMovie.isValid():
            if self.__animationMovie.state() == QtGui.QMovie.NotRunning or self.__animationMovie.state() == QtGui.QMovie.Paused:
                self.__animationMovie.start()
                self.setHidden(False)

    def _stop(self):
        if self.__animationMovie.isValid():
            if self.__animationMovie.state() == QtGui.QMovie.Running:
                self.__animationMovie.stop()
                self.setHidden(True)

