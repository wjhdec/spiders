# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class WpfItem(scrapy.Item):
    class_name = Field()
    class_type = Field()
    class_desc = Field()
    namespace = Field()
    class_props = Field()
