from scrapy import cmdline
import time

localtime = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))

cmdline.execute('scrapy crawl books -o books-{}.csv'.format(localtime).split())
