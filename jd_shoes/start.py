from scrapy import cmdline

# 不显示日志（含报错信息）执行爬虫
cmdline.execute('scrapy crawl jd --nolog'.split())