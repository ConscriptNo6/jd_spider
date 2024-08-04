from scrapy import cmdline

cmdline.execute('scrapy crawl jd'.split())

# 不显示日志（含报错信息）执行爬虫
# cmdline.execute('scrapy crawl jd --nolog'.split())