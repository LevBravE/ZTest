#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from HTMLParser import HTMLParser

#**************************************************************************************************
# class: HtmlContent
#**************************************************************************************************

class HtmlContent(HTMLParser):
    """
    Получаем содержимое тега <body></body>
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.__flagContent = False
        self.__strContent = ''
        self.__strContentNotImg = ''
        self.__lstImages = []

    def _clear(self):
        self.__flagContent = False
        self.__strContent = ''
        self.__strContentNotImg = ''
        self.__lstImages = []

    def _content(self):
        return self.__strContent

    def _contentNotImg(self):
        return self.__strContentNotImg

    def _img(self):
        return self.__lstImages

    def handle_starttag(self, tag, attrs):
        if tag != 'meta' and tag != 'a' and tag != 'img':
            strAttrs = ''

            for attribute in attrs:
                if attribute[0] != 'style':
                    strAttrs += '%s="%s"' % (attribute[0], attribute[1])

            self.__strContentNotImg += '<%s %s>' % (tag, strAttrs)

        if self.__flagContent:
            strAttrs = ''

            for attribute in attrs:
                if attribute[0] != 'style':
                    strAttrs += '%s="%s"' % (attribute[0], attribute[1])

            self.__strContent += '<%s %s>' % (tag, strAttrs)

        if tag == 'body':
            self.__flagContent = True

    def handle_startendtag(self, tag, attrs):
        if tag != 'img':
            self.__strContentNotImg += self.get_starttag_text()

        if self.__flagContent:
            if tag != 'br':
                self.__strContent += self.get_starttag_text()

        if tag == 'img':
            for attribute in attrs:
                if attribute[0] == 'src':
                    self.__lstImages.append(attribute[1])

    def handle_data(self, data):
        self.__strContentNotImg += data

        if self.__flagContent:
            self.__strContent += data

    def handle_endtag(self, tag):
        if tag != 'meta' and tag != 'a' and tag != 'img':
            self.__strContentNotImg += '</%s>' % tag

        if tag == 'body':
            self.__flagContent = False

        if self.__flagContent:
            self.__strContent += '</%s>' % tag


if __name__ == '__main__':
    parser = HtmlContent()
    parser.feed('<html><head><title>Test</title></head>'
                '<body><h1 style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;" id="dd">Parse me!</h1><p><br />ddd</p></body></html>')

    print parser._content()
    print parser._img()