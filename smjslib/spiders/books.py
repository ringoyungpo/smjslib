# -*- coding: utf-8 -*-
import scrapy
import re

def parse_books_imformation(response):
    book_info = response.css('#ctl00_ContentPlaceHolder1_bookcardinfolbl').xpath('string(.)').extract()[0].split(
        '\u3000')
    book_info = list(filter(lambda item: item, book_info))

    isbnandprice = str(book_info[-5])
    isbn = isbnandprice.split('：')[0]
    isbn = re.match(r'ISBN[\w|-]+', isbn).group(0)

    price = isbnandprice.split('：')[1][3:]
    price = re.match('\d+?.\d{2}', price).group(0)

    titles = str(book_info[-4]).split('．')[-1]
    titles = re.split(r'[①-⑳]', titles)
    titles.remove('')

    authors = str(book_info[-3]).split('．')[-1]
    authors = re.split(r'[①-⑳]', authors)
    authors = list(map(lambda author: author.strip(','), authors))
    authors = list(filter(lambda author: author, authors))

    tags = str(book_info[-2]).split('．')[-1]
    tags = re.split(r'[①-⑳]', tags)
    tags.remove('')
    tags = list(map(lambda taglist: taglist.split('  - '), tags))
    tags = sum(tags, [])
    tags = list(set(tags))

    associations = str(book_info[-1]).split('．')[-1][1:]
    associations = re.split(r'[①-⑳]', associations)
    associations = list(map(lambda association:re.match(r'\w+[.\w+]+', association).group(0), associations))
    associations = list(filter(lambda association: association, associations))

    if isbn and price:
        yield {
            'isbn': isbn,
            'price': price,
            'titles': titles,
            'authors': authors,
            'tags': tags,
            'associations': associations
        }


def parse_books_url(response):
    for href in response.css('td span.title a::attr(href)'):
        yield response.follow(href, parse_books_imformation)


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['smjslib.jmu.edu.cn']
    start_urls = ['http://smjslib.jmu.edu.cn/top100.aspx?sparaname=anywords']

    def parse(self, response):
        for href in response.css('td a::attr(href)'):
            yield response.follow(href, parse_books_url)
