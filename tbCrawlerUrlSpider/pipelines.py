# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os
from hashlib import md5

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from twisted.enterprise import adbapi

from tbCrawlerUrlSpider import settings
import traceback
# from scrapy.conf import settings


class TbcrawlerurlspiderPipeline(object):
    def __init__(self):
        if not os.path.exists(settings.IMAGES_STORE):
            os.makedirs(settings.IMAGES_STORE)
        file_name = '%s/%s' % (settings.IMAGES_STORE, "taobao.json")
        self.file = codecs.open(file_name, 'w', encoding='utf-8')
        #dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), indent=4, separators=(',', ': '), ensure_ascii=False)
        self.file.write(line)
        return item


class MySQLStoreTbUrlPipeline(object):
    insert_sql = '''insert into tb_urls_crawler(id, pid, url, depth, max_depth, create_time) values(%s, %s, %s, %s, %s, %s)'''
    query_max_id = '''select max(id) as maxid from tb_urls_crawler where 1=1'''
    last_id = 0
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dbargs = settings.DB_CONNECT
        db_server = settings.DB_SERVER
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)
        self.dbpool = dbpool
        # d = self.dbpool.runInteraction(self._do_query)
        # d.addErrback(self._handle_error)

    def spider_closed(self, spider):
        self.dbpool.close()

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_insert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行写入数据库中
    def _do_insert(self, conn, item, spider):
        try:
            conn.execute(self.insert_sql, (item['id'], item['pid'], item['url'], item['depth'], item['max_depth'], item['create_time']))
        except:
            print traceback.format_exc()
            print 'error to execute'

    def _do_query(self,conn):
        try:
            conn.execute(self.query_max_id)
            ret = conn.fetchone()
            if ret:
                print ret[0]
            print ret
        except:
            print traceback.format_exc()
            print 'failed to query'

    # 获取url的md5编码
    def _get_linkmd5id(self, item):
        # url进行md5处理，为避免重复采集设计
        return md5(item['url']).hexdigest()

    # 异常处理
    def _handle_error(self, failue, item, spider):
        print failue
