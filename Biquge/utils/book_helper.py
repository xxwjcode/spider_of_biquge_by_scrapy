# -*- coding: utf-8 -*-
__author__ = 'xwj'
__date__ = '2019/3/18 0018 16:32'

import re


chapter_pattern = re.compile('www.\w+?.\w+?/(\d*)/(\d*)/(\d*).')
book_pattern = re.compile('www.\w+?.\w+?/(\d*)/(\d*)/')


class get_bookid_by_chapter():
    def __init__(self, url):
        self.result = re.findall(chapter_pattern, url)

    @property
    def book_id(self):
        return self.result[0][1]

    @property
    def book_year(self):
        return self.result[0][0]

    @property
    def chapter_id(self):
        return self.result[0][2]


class get_bookid_by_book():
    def __init__(self, url):
        self.result = re.findall(book_pattern, url)

    @property
    def book_id(self):
        return self.result[0][1]

    @property
    def book_year(self):
        return self.result[0][0]


def get_trueName(str):
    return str.strip('作\xa0\xa0\xa0\xa0者：')


if __name__ == '__main__':
    url = 'http://www.xbiquge.la/10/10489/4534454.html'
    a = get_bookid(url)
