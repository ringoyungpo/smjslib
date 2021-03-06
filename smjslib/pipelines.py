# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymysql import connect

#该管道可以将数据传入数据库
class SmjslibPipeline(object):
    def __init__(self):
        #定义链接数据库信息
        self.connect = connect(
            host='localhost',
            db='smjslib',
            user='root',
            password='root',
            port=3306,
            charset='utf8',
            use_unicode=True)

        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        sql = r"SELECT * FROM books WHERE isbn='{}'".format(item['isbn'])
        self.cursor.execute(sql)
        repetition = self.cursor.fetchone()、
        #若存在该书籍信息则不存储，否则存储
        if repetition:
            pass
        else:
            try:
                sql = r"INSERT INTO books(title, author, publisher_city, publisher,publish_year, pages, length, isbn, price, titles, authors, tags, association, total, available, loan, frequence)VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {})".format(
                    item['title'], item['author'], item['publisher_city'], item['publisher'], item['publish_year'],
                    item['pages'], item['length'], item['isbn'], item['price'], ','.join(item['titles']),
                    ','.join(item['authors']), ','.join(item['tags']), item['association'], item['total'],
                    item['available'], item['loan'], item['frequence'])
                self.cursor.execute(sql)
                self.connect.commit()
                #存储标签信息在单独的表内
                for tag in item['tags']:
                    sql = r"INSERT INTO tags(isbn, tag)VALUES('{}', '{}')".format(
                        item['isbn'], tag)
                    self.cursor.execute(sql)
                    self.connect.commit()
                #存储作者信息在单独的表内
                for author in item['authors']:
                    sql = r"INSERT INTO authors(isbn, author)VALUES('{}', '{}')".format(
                        item['isbn'], author)
                    self.cursor.execute(sql)
                    self.connect.commit()
            except Exception as error:
                print(error)
        return item
