# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


# class SmjslibItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass


class SmjslibItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    author = Field()
    publisher_city = Field()
    publisher = Field()
    publish_year = Field()
    pages = Field()
    length = Field()
    isbn = Field()
    price = Field()
    titles = Field()
    authors = Field()
    tags = Field()
    association = Field()
    total = Field()
    available = Field()
    loan = Field()
    frequence = Field()
    # pass