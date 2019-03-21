# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from Biquge.utils.book_helper import get_bookid_by_chapter, get_bookid_by_book, get_trueName
from Biquge.utils.get_md5 import get_md5
from Biquge.items import BiqugeBookItem2, BiqugeChapterItem2, BaseItemLoader
import datetime


class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['xbiquge.la']
    # start_urls = ['http://www.xbiquge.la/10/10489/']
    # start_urls = ['http://www.xbiquge.la/0/52/']
    start_urls = ['http://www.xbiquge.la/15/15409/']

    def parse(self, response):
        book_id = get_bookid_by_book(response.url).book_id
        publish_year = get_bookid_by_book(response.url).book_year

        book_item_loader = BaseItemLoader(item=BiqugeBookItem2(), response=response)
        book_item_loader.add_css('tag', '.con_top a::text')
        book_item_loader.add_css('title', '#info h1::text')
        book_item_loader.add_css('author', '#info p::text')
        book_item_loader.add_css('image', '#fmimg img::attr(src)')
        book_item_loader.add_css('des', '#intro p::text')
        book_item_loader.add_value('book_id', book_id)
        book_item_loader.add_value('publish_year', publish_year)
        book_item_loader.add_value('url', response.url)
        book_item_loader.add_value('url_object_id', get_md5(response.url))
        book_item = book_item_loader.load_item()
        yield book_item

        # 获取推荐书籍url，生产request对象
        book_urls1 = response.css('#listtj a::attr(href)').extract()
        book_urls2 = response.css('.footer_link a::attr(href)').extract()
        for book_url in book_urls1+book_urls2:
            yield scrapy.Request(url=parse.urljoin(response.url, book_url), callback=self.parse)

        # 获取书籍章节url，并生成url对象
        chapter_list = response.css('#list dd a::attr(href)').extract()
        for chapter_url in chapter_list:
            yield scrapy.Request(url=parse.urljoin(response.url, chapter_url), callback=self.parse_detail)

    def parse_detail(self, response):
        '''书籍章节response解析'''
        response = response.replace(body=response.body.replace(b'<br>', b'\n'))
        book_id = get_bookid_by_chapter(response.url).book_id
        publish_year = get_bookid_by_chapter(response.url).book_year
        chapter_id = get_bookid_by_chapter(response.url).chapter_id

        chapter_item_loader = BaseItemLoader(item=BiqugeChapterItem2(), response=response)
        chapter_item_loader.add_css('title', '.bookname h1::text')
        chapter_item_loader.add_css('content', '#content::text')
        chapter_item_loader.add_value('book_id', book_id)
        chapter_item_loader.add_value('publish_year', publish_year)
        chapter_item_loader.add_value('chapter_id', chapter_id)
        chapter_item_loader.add_value('url', response.url)
        chapter_item_loader.add_value('url_object_id', get_md5(response.url))
        chapter_item_loader.add_value('add_time', datetime.datetime.now())
        chapter_item = chapter_item_loader.load_item()

        yield chapter_item
