# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TbcrawlerurlspiderItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    pid = scrapy.Field()
    url = scrapy.Field()
    depth = scrapy.Field()
    max_depth = scrapy.Field()
    create_time = scrapy.Field()
