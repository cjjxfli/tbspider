# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from tbCrawlerGoodsSpider import settings
import codecs
import json
import os
from hashlib import md5
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from twisted.enterprise import adbapi
import traceback
from tbCrawlerUrlSpider.deps.tbUtils import *

class TbcrawlergoodsspiderPipeline(object):
    def __init__(self):
        if not os.path.exists(settings.IMAGES_STORE):
            os.makedirs(settings.IMAGES_STORE)
        file_name = '%s/%s' % (settings.IMAGES_STORE,"taobao.json")
        self.file = codecs.open(file_name, 'w', encoding='utf-8')
        self.json_array = []
        #dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), indent=4, separators=(',', ': '), ensure_ascii=False)
        self.file.write(line)
        return item


class MySQLStoreTbGoodsPipeline(object):
    insert_sql = '''insert into tb_goods_crawler(id, shop_name, shop_url, shop_age, seller_name,
 goods_title,goods_url,goods_commets_count,goods_sales_count,goods_img_url,
 goods_local_img_path,goods_old_price,goods_now_price,goods_details,create_time)
  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dbargs = settings.DB_CONNECT
        db_server = settings.DB_SERVER
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)
        self.dbpool = dbpool

    def spider_closed(self, spider):
        self.dbpool.close()

    # pipeline默认调用
    def process_item(self, item, spider):
        # 保存图片
        image_url = item["goods_img_url"]
        if strcmp(image_url,'') != 0:
            dir_path = '%s/%s' % (settings.IMAGES_STORE, 'images')
            us = image_url.split('/')[3:]
            image_file_name = '_'.join(us)
            print "file name %s " % image_file_name
            file_path = '%s/%s' % (dir_path, image_file_name)
            if not os.path.exists(file_path):
                with open(file_path, 'ab') as handle:
                    header = {
                        'Referer': image_url,
                        # 这个referer必须要，不然get不到这个图片
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
                    }
                response = requests.get(image_url, headers=header)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
                handle.close()
                item['goods_local_img_path'] = file_path

        d = self.dbpool.runInteraction(self._do_insert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行写入数据库中
    def _do_insert(self, conn, item, spider):
        try:
            conn.execute(self.insert_sql, (item['id'], item['shop_name'], item['shop_url'], item['shop_age'], item['seller_name'],
                                           item['goods_title'], item['goods_url'], item['goods_commets_count'], item['goods_sales_count'],item['goods_img_url'],
                                           item['goods_local_img_path'], item['goods_old_price'], item['goods_now_price'], item['goods_details'],item['create_time']))
        except:
            print traceback.format_exc()
            print 'error to execute'

    # 获取url的md5编码
    def _get_linkmd5id(self, item):
        # url进行md5处理，为避免重复采集设计
        return md5(item['url']).hexdigest()

    # 异常处理
    def _handle_error(self, failue, item, spider):
        print failue