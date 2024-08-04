from typing import Iterable
import scrapy
import re
from jd_shoes.items import JdShoesItem

class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]

    def start_requests(self):
        yield scrapy.Request(url='https://list.jd.com/list.html?cat=1318,12099,9756', callback=self.search_page_parse)

    # 处理搜索页面
    def search_page_parse(self, response):

        # for循环遍历每件商品
        for li in response.xpath('//*[@id="J_goodsList"]/ul/li'):
            item = JdShoesItem()

            title = li.xpath('./div/div/a/em/text()').extract()[0] # 标题
            price = li.xpath('./div/div/strong/i/text()').extract()[0] # 价格
            skuid = li.xpath('./@data-sku').extract()[0] # 商品ID
            details_url = li.xpath('./div/div[@class="p-img"]/a/@href').extract()[0] # 详情页url

            # 将数据存储到item对象中
            item['title'] = title
            item['price'] = price
            item['skuid'] = skuid
            item['details_url'] = details_url

            # 如果url不是以“https:”开头，就补全
            if not item['details_url'].startswith('https:'):
                item['details_url'] = 'https:' + item['details_url']
            
            yield scrapy.Request(item['details_url'], callback=self.details_page_parse, meta={"item": item})

    # 处理商品详情页页面
    def details_page_parse(self, response):
        item = response.meta['item']

        # 定义两个列表分别存储颜色和尺码
        color_list = []
        size_list = []

        # 遍历所有颜色，合并成一个列表，存储到item对象中
        for color in response.xpath('//*[@id="choose-attrs"]/div[@id="choose-attr-1"]/div[@class="dd"]/div'):
            color_list.append(color.xpath('@data-value').extract()[0])
        item['color'] = color_list

        # 遍历所有尺码，合并成一个列表，存储到item对象中
        for size in response.xpath('//*[@id="choose-attrs"]/div[@id="choose-attr-2"]/div[@class="dd"]/div'):
            size_list.append(size.xpath('@data-value').extract()[0])
        item['size'] = size_list
        
        # 补全接口url并发起请求，所有商品介绍图url都保存在返回的json字符串中
        skuid = item['skuid']
        mainskuid = self.get_mainskuid(response)
        details_img_req_url = f'https://api.m.jd.com/description/channel?appid=item-v3&functionId=pc_description_channel&skuId={skuid}&mainSkuId={mainskuid}&charset=utf-8&cdn=2&callback=showdesc'

        # 调用details_img_parse函数处理json字符串
        yield scrapy.Request(details_img_req_url, callback=self.details_img_parse, meta={"item": item})
        
    # 解析商品详介绍url
    def details_img_parse(self, response):
        item = response.meta['item']
        details_img_find_result = re.findall('//img[0-9]*.360buyimg.com/[^<>\s]*\.jpg|png', response.body.decode(response.encoding))
        
        # 给所有url添加上“https:”前缀
        for i in range(len(details_img_find_result)):
            details_img_find_result[i] = 'https:' + details_img_find_result[i]
        item['img_urls'] = details_img_find_result

        yield item
        
    # 获取商品的mainSkuid
    def get_mainskuid(self, response):
        search_result = re.search("mainSkuId:'(\d+)'", response.body.decode(response.encoding))[0]
        mainskuid = re.search(r'\d+', search_result)[0]
        return mainskuid