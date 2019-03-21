# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader


# 采用itemloader方式处理item
class BaseItemLoader(ItemLoader):
    '''自定义ItemLoader, 默认输出取列表的第一个元素'''
    default_output_processor = TakeFirst()


# 自定义的一些方法函数
def TakeByIndex(index):
    '''根据索引取值，不存在则返回None'''
    def TakeValue(values):
        try:
            return values[index]
        except Exception as e:
            return None
    return TakeValue


def Authorstrip(value):
    return value.split('：')[-1].strip(' ')


def ChapterTitlestrip(value):
    return value.strip('正文卷 ')


def Str_to_list(values):
    '''将输入列表返回以列表只有第一个元素的列表，imageurl字段需要列表'''
    try:
        return [values[0]]
    except Exception as e:
        return None


class BiqugeBookItem2(scrapy.Item):
    tag = scrapy.Field(
        output_processor=TakeByIndex(1)
    )
    title = scrapy.Field()
    author = scrapy.Field(
        input_processor=MapCompose(Authorstrip,)
    )
    image = scrapy.Field(
        output_processor=Str_to_list
    )
    image_local = scrapy.Field()
    des = scrapy.Field(
        output_processor=TakeByIndex(-1)
    )
    book_id = scrapy.Field()
    publish_year = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    def do_sql_insert(self):
        '''对应的item执行的sql语句与参数'''
        insert_sql = """
                        insert into books_book
                        (tag, title, author, image, image_local, des, book_id, publish_year, url, url_object_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
        params = (
            self['tag'], self['title'], self['author'], self['image'], self['image_local'], self['des'], self['book_id'],
            self['publish_year'], self['url'], self['url_object_id'])
        return insert_sql, params


class BiqugeChapterItem2(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(ChapterTitlestrip, )
    )
    content = scrapy.Field(
        output_processor=Join('\n')
    )
    book_id = scrapy.Field()
    publish_year = scrapy.Field()
    chapter_id = scrapy.Field()
    add_time = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    def do_sql_insert(self):
        '''对应的item执行的sql语句与参数'''
        insert_sql = """
                        insert into books_chapter
                        (title, content, book_id_id, publish_year, chapter_id, add_time, url, url_object_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                    """
        params = (
            self['title'], self['content'], self['book_id'], self['publish_year'], self['chapter_id'], self['add_time'], self['url'],
            self['url_object_id'])
        return insert_sql, params