# -*- coding: utf-8 -*-
__author__ = 'xwj'
__date__ = '2019/3/18 0018 21:21'

import MySQLdb


conn = MySQLdb.connect('127.0.0.1', 'root', 'woshinibaba', 'biquge', charset="utf8", use_unicode=True)
cursor = conn.cursor()

insert_sql = """
            insert into books_book (book_id, title, author, tag)
            VALUES (%s, %s, %s, %s)
        """
cursor.execute(insert_sql, ("book_id", "title", "author", "tag"))
conn.commit()
print(1)
print(len('333906e2a9f58927412540da3eae47c204bc45e1.jpg'))