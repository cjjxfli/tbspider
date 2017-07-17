# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TbcrawlergoodsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
    shop_age = scrapy.Field()
    seller_name = scrapy.Field()
    goods_title = scrapy.Field()
    goods_url = scrapy.Field()
    goods_commets_count = scrapy.Field()
    goods_sales_count = scrapy.Field()
    goods_img_url = scrapy.Field()
    goods_local_img_path = scrapy.Field()
    goods_old_price = scrapy.Field()
    goods_now_price = scrapy.Field()
    goods_details = scrapy.Field()
    create_time = scrapy.Field()
