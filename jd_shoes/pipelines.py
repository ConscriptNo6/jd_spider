# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os

# 获取本文件的绝对路径
absolute_file_path = os.path.dirname(__file__)

class JsonLinesPipeline:

    def open_spider(self, spider):
        # 打开和本文件在同一目录下的JSON文件
        self.file = open(absolute_file_path + '/result_data.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 将item转换为字典，并转换为JSON格式的字符串
        line = json.dumps(dict(item), ensure_ascii=False,) + "\n"
        # 写入文件
        self.file.write(line)
        # 必须返回一个item对象
        return item
    
    def close_spider(self, spider):
        # 关闭文件
        self.file.close()

# 弃用
# class JdShoesPipeline:
#     def process_item(self, item, spider):
#         print(item)
#         return item
