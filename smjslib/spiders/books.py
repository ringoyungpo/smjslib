# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.parse import urlencode
from smjslib.items import SmjslibItem

#爬取解析每一页的关键信息
def parse_books_imformation(response):

    book_info = response.css('#ctl00_ContentPlaceHolder1_bookcardinfolbl').xpath('string(.)').extract()[0].split(
        '\u3000')
    book_info = list(filter(lambda item: item, book_info))

    title_author_publishment = re.split('／|．—', book_info[0])
    #标题
    title = title_author_publishment[0]
    #作者
    author = title_author_publishment[1]
    publishment = title_author_publishment[-1].split('；')[0]
    #出版城市
    publisher_city, publisher, publish_year = re.split('：|，', publishment)
    #出版年份
    publish_year = re.search(r'\d{4}', publish_year).group()

    pages_length = re.split('；', book_info[1])
    pages = re.findall('\d\d+', pages_length[0])
    #总页数
    pages = max(pages)
    #书籍长度
    length = re.search('\d\d+', pages_length[1]).group()

    isbnandprice = str(book_info[-5])
    #isbn码
    isbn = isbnandprice.split('：')[0]
    isbn = re.search(r'ISBN[\w|-]+', isbn).group()

    #价格
    price = isbnandprice.split('：')[1]
    price = re.search(r'\d+.?\d+', price).group()

    #相关标题
    titles = str(book_info[-4]).split('．')[-1]
    titles = re.split(r'[①-⑳]', titles)
    titles.remove('')

    #相关作者
    authors = str(book_info[-3]).split('．')[-1]
    authors = re.split(r'[①-⑳]', authors)
    authors = list(map(lambda author: author.strip(','), authors))
    authors = list(filter(lambda author: author, authors))

    #相关标签
    tags = str(book_info[-2]).split('．')[-1]
    tags = re.split(r'[①-⑳]', tags)
    tags.remove('')
    tags = list(map(lambda taglist: re.split('  - |-', taglist), tags))
    tags = sum(tags, [])
    tags = list(set(tags))

    #索引码
    association = response.xpath('//*[@id="bardiv"]/div/table/tbody/tr[1]/td[2]/text()').extract()[0].split('/')[0]
    association = re.search(r'\w+[.\w+]+[-\w+]+', association).group()

    #馆藏量用馆藏链接数量表示
    total = len(response.xpath('//*[@id="bardiv"]/div/table/tbody/tr[*]/td[1]/a'))
    #借出量用借出链接数量表示
    loan = len(response.xpath('//*[@id="bardiv"]/div/table/tbody/tr[*]/td[6]/a'))
    #近一年的借出数量
    frequence = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_blclbl"]/text()').extract()[0]
    item = SmjslibItem()
    if isbn and price and association:
        item['title'] = title
        item['author'] = author
        item['publisher_city'] = publisher_city
        item['publisher'] = publisher
        item['publish_year'] = publish_year
        item['pages'] = pages
        item['length'] = length
        item['isbn'] = isbn
        item['price'] = price
        item['titles'] = titles
        item['authors'] = authors
        item['tags'] = tags
        item['association'] = association
        item['total'] = total
        item['available'] = total - loan
        item['loan'] = loan
        item['frequence'] = frequence
        yield item

#将该页中的书本信息进行爬取解析
def parse_books_url(response):
    for href in response.css('td span.title a::attr(href)'):
        yield response.follow(href, parse_books_imformation)

#获取该热词的搜索结果总页数，进行该热词每一页的爬取
def parse_books_pages(response):
    pages = len(response.css('#ctl00_ContentPlaceHolder1_gotoddlfl1 > option'))
    anywords = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_conditionlbl"]/font/text()').extract()[0]
    body = {'anywords': anywords,
            'dt': 'ALL',
            'cl': 'ALL',
            'dp': '20',
            'sf': 'M_PUB_YEAR',
            'ob': 'DESC',
            'sm': 'table',
            'dept': 'ALL'}

    for page in range(1, pages + 1):
        body['page'] = page
        url = 'http://smjslib.jmu.edu.cn/searchresult.aspx?{}'.format(urlencode(body, encoding='gb2312'))
        yield scrapy.Request(url, parse_books_url)


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['smjslib.jmu.edu.cn']

    #定义要爬取的网址入口
    start_urls = ['http://smjslib.jmu.edu.cn/top100.aspx?sparaname=anywords']

    #将这100个搜索热词的搜索结果进行爬取
    def parse(self, response):
        for href in response.css('td a::attr(href)'):
            yield response.follow(href, parse_books_pages)
