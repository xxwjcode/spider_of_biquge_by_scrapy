# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from  scrapy.pipelines.images import ImagesPipeline
import codecs
import json


class BiqugeBookItemImagePipeline(ImagesPipeline):
    '''继承内置的 ImagesPipeline ，自动进行图片下载并将下载后图片的存放路径
    赋值给在item[self.images_result_field]'''
    def item_completed(self, results, item, info):
        if 'image' in item:
            if isinstance(item, dict) or self.images_result_field in item.fields:
                # item[self.images_result_field] = [x for ok, x in results if ok]
                for ok, x in results:
                    if ok:
                        item[self.images_result_field] = x.get('path')
        return item


class JsonWithEncodePipeline(object):
    '''自定义jsonexporter导出'''
    def __init__(self):
        self.file = codecs.open('book.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if isinstance(item, BiqugeBookItem):
            lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(lines)
        return item

    def spider_closed(self):
        self.file.close()


from scrapy.exporters import JsonItemExporter, XmlItemExporter


class JsonItemPipeline(object):
    '''利用内置的JsonItemExporter类进行数据json类型保存'''
    def __init__(self):
        self.file = open('book2.json', 'wb')
        self.exporter = JsonItemExporter(file=self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class XmlItemPipeline(object):
    '''利用内置的JsonItemExporter类进行数据json类型保存'''
    def __init__(self):
        self.file = open('book2.xml', 'wb')
        self.exporter = XmlItemExporter(file=self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

import MySQLdb
import MySQLdb.cursors


class MysqlPipeline(object):
    def __init__(self):
        '''建立数据库连接，并生成游标'''
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'woshinibaba', 'biquge', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        '''取出item中对应的sql操作语句与参数，并保存到数据库'''
        insert_sql, params = item.do_sql_insert()
        self.cursor.execute(insert_sql, params)
        self.conn.commit()
        return item


from twisted.enterprise import adbapi


class MysqlTwistedPipline(object):
    '''异步twisted插入数据库'''
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''从setting文件中取出相应参数，生存连接池'''
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        '''执行具体的插入
        根据不同的item 从item中取出各自自定义的sql语句与参数并执行中
        '''
        insert_sql, params = item.do_sql_insert()
        cursor.execute(insert_sql, params)
