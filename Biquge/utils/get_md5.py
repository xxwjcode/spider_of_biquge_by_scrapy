# -*- coding: utf-8 -*-
__author__ = 'xwj'
__date__ = '2019/3/18 0018 18:48'
from hashlib import md5


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
        m = md5()
        m.update(url)
        return m.hexdigest()


if __name__ == '__main__':
    url = 'sFA SASASA'
    print(get_md5(url))