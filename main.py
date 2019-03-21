# -*- coding: utf-8 -*-
__author__ = 'xwj'
__date__ = '2019/3/18 0018 16:23'

from scrapy.cmdline import execute
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'biquge', '--nolog'])
execute(['scrapy', 'crawl', 'biquge'])