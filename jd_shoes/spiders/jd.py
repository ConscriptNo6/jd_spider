from typing import Iterable
import scrapy
from jd_shoes.items import JdShoesItem

class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = ["https://list.jd.com/list.html?cat=1318,12099,9756"]

    # def start_requests(self):
    #     yield scrapy.Request(self.url)
    
    def parse(self, response):

        # for循环遍历每件商品
        for li in response.xpath('//*[@id="J_goodsList"]/ul/li'):
            item = JdShoesItem()

            title = li.xpath('./div/div/a/em/text()').extract()[0] # 标题
            price = li.xpath('./div/div/strong/i/text()').extract()[0] # 价格
            sku = li.xpath('./@data-sku').extract()[0] # 商品ID
            details_url = li.xpath('./div/div[@class="p-img"]/a/@href').extract()[0] # 详情页url

            # 将数据存储到item对象中
            item['title'] = title
            item['price'] = price
            item['sku'] = sku
            item['details_url'] = details_url

            # 如果url不是以“https:”开头，就补全
            if not item['details_url'].startswith('https:'):
                item['details_url'] = 'https:' + item['details_url']
            
            yield scrapy.Request(item['details_url'], callback=self.info_parse, meta={"item": item})

    def info_parse(self, response):
        item = response.meta['item']

        # 定义两个列表分别存储颜色和尺码
        color_list = []
        size_list = []

        # 遍历所有颜色并合并成一个列表
        for color in response.xpath('//*[@id="choose-attrs"]/div[@id="choose-attr-1"]/div[@class="dd"]/div'):
            color_list.append(color.xpath('@data-value').extract()[0])
        item['color'] = color_list

        # 遍历所有尺码并合并成一个列表
        for size in response.xpath('//*[@id="choose-attrs"]/div[@id="choose-attr-2"]/div[@class="dd"]/div'):
            size_list.append(size.xpath('@data-value').extract()[0])
        item['size'] = size_list

        yield item