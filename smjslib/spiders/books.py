# -*- coding: utf-8 -*-
import scrapy
import re


def parse_books_imformation(response):
    book_info = response.css('#ctl00_ContentPlaceHolder1_bookcardinfolbl').xpath('string(.)').extract()[0].split(
        '\u3000')
    book_info = list(filter(lambda item: item, book_info))

    title_author_publishment = re.split('／|．—', book_info[0])
    title = title_author_publishment[0]
    author = title_author_publishment[1]
    publishment = title_author_publishment[-1]
    publisher_city, publisher, publish_year = re.split('：|，', publishment)
    publish_year = re.search(r'\d{4}', publish_year).group()

    pages_length = re.split('；', book_info[1])
    pages = re.findall('\d\d+', pages_length[0])
    pages = max(pages)
    length = re.search('\d\d+', pages_length[1]).group()

    isbnandprice = str(book_info[-5])
    isbn = isbnandprice.split('：')[0]
    isbn = re.search(r'ISBN[\w|-]+', isbn).group()

    price = isbnandprice.split('：')[1]
    price = re.search(r'\d+.?\d+', price).group()

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

    association = response.xpath('//*[@id="bardiv"]/div/table/tbody/tr[1]/td[2]/text()').extract()[0].split('/')[0]
    association = re.search(r'\w+[.\w+]+[-\w+]+', association).group()

    total = len(response.xpath('//*[@id="bardiv"]/div/table/tbody/tr[*]/td[1]/a'))
    loan = len(response.xpath('//*[@id="bardiv"]/div/table/tbody/tr[*]/td[6]/a'))
    frequence = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_blclbl"]/text()').extract()[0]

    if isbn and price and association:
        yield dict(title=title, author=author, publisher_city=publisher_city, publisher=publisher,
                   publish_year=publish_year, pages=pages, length=length, isbn=isbn, price=price, titles=titles,
                   authors=authors, tags=tags,
                   association=association, total=total, available=total - loan, loan=loan, frequence=frequence)


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
