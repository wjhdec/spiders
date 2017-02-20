# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArcgiswpfPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.line-json', 'wb')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(bytes(line, encoding = "utf8"))
        return item
    def spider_closed(self, spider):
        self.file.close()