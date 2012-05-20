#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from fs.zipfs import ZipFS
from fs.errors import ResourceNotFoundError

#**************************************************************************************************
# class: ZipArchive
#**************************************************************************************************

class ZipArchive(ZipFS):
    """
    Zip API
    """

    def _write(self, dictImageNames):
        """
        Запись файлов в zip архив
        """
        try:
            fileMainName = u'main.xml'
            fileMain = self.open(fileMainName, 'w')
            fileMain.write(dictImageNames[fileMainName])
            del dictImageNames[fileMainName]
            fileMain.close()

            dirImg = self.makeopendir('img')

            for fileName, fileData in dictImageNames.items():
                if not fileName in dirImg.listdir():
                    fileImg = dirImg.open(fileName, 'w')
                    fileImg.write(fileData)
                    fileImg.close()

            for fileName in dirImg.listdir():
                if not fileName in dictImageNames.keys():
                    dirImg.remove(fileName)

            dirImg.close()
        except ResourceNotFoundError:
            return False

        return True

    def _read(self):
        """
        Чтение файлов в zip архиве
        """
        dictImageNames = {}

        try:
            fileMainName = u'main.xml'
            fileMain = self.open(fileMainName)
            dictImageNames[fileMainName] = fileMain.read()
            fileMain.close()

            if u'img' in self.listdir():
                dirImg = self.opendir('img')

                for fileName in dirImg.listdir():
                    fileImg = dirImg.open(fileName)
                    dictImageNames[fileName] = fileImg.read()
                    fileImg.close()

                dirImg.close()
        except ResourceNotFoundError:
            return False

        return dictImageNames


if __name__ == '__main__':
    zipFile = ZipArchive('~/hello.ztest')
    dictImageNames = zipFile._read()
    zipFile.close()