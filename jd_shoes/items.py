# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JdShoesItem(scrapy.Item):
    title = scrapy.Field() # 标题
    price = scrapy.Field() # 价格
    skuid = scrapy.Field() # 商品ID
    details_url = scrapy.Field() # 详情页url

    # 具体是什么内容，题目中没有明确说明
    details = scrapy.Field() # 详情

    color = scrapy.Field() # 颜色
    size = scrapy.Field() # 尺码
    img_urls = scrapy.Field() # 商品介绍图url