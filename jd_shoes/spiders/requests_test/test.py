# 比较混乱，仅做测试用

import requests
from lxml import etree
import os

# 获取本文件的绝对路径
absolute_file_path = os.path.dirname(__file__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Cookie": "填入你的cookies",
}

# 搜索页
def search_page():
    url = "https://list.jd.com/list.html?cat=1318,12099,9756"
    res = requests.get(url=url, headers=headers)

    # 将网页源码保存到本文件同目录下
    with open(absolute_file_path + '/search_page.html', 'w', encoding='utf-8') as f:
        f.write(res.text)

    root_element = etree.HTML(res.text)

    # 遍历每件商品并提取信息
    for li in root_element.xpath('//*[@id="J_goodsList"]/ul/li'):
        title = li.xpath('./div/div/a/em/text()') # 标题
        price = li.xpath('./div/div/strong/i/text()') # 价格
        sku = li.xpath('./@data-sku') # ID
        url = li.xpath('./div/div[@class="p-img"]/a/@href') # 商品详情页url
        print(title,price, sku, url)

# 商品详情页
def details_page():
    color_list = []
    size_list = []
    url = "https://item.jd.com/10048683391525.html"
    res = requests.get(url=url, headers=headers)

    # 将网页源码保存到本文件同目录下
    with open(absolute_file_path + '/details_page.html', 'w', encoding='utf-8') as f:
        f.write(res.text)

    root_element = etree.HTML(res.text)

    # 遍历所有颜色
    for color in root_element.xpath('//*[@id="choose-attrs"]/div[@id="choose-attr-1"]/div[@class="dd"]/div'):
        color_list.append(color.xpath('@data-value')[0])

    # 遍历所有尺码
    for size in root_element.xpath('//*[@id="choose-attrs"]/div[@id="choose-attr-2"]/div[@class="dd"]/div'):
        size_list.append(size.xpath('@data-value')[0])

    return color_list, size_list

# print(search_page())
details_page()