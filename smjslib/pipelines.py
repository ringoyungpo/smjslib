# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymysql import connect


class SmjslibPipeline(object):
    def __init__(self):
        self.connect = connect(
            host='localhost',
            db='smjslib',
            user='root',
            password='tiger',
            port=3306,
            charset='utf8',
            use_unicode=True)

        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        print(item)
        sql = r"INSERT INTO books(title, author, publisher_city, publisher,publish_year, pages, length, isbn, price, titles, authors, tags, association, total, available, loan, frequence)VALUES('{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {})".format(
            item['title'], item['author'], item['publisher_city'], item['publisher'], item['publish_year'],
            item['pages'], item['length'], item['isbn'], item['price'], ','.join(item['titles']),
            ','.join(item['authors']), ','.join(item['tags']), item['association'], item['total'], item['available'],
            item['loan'], item['frequence'])
        try:
            print(sql)
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as error:
            print(error)

        return item
