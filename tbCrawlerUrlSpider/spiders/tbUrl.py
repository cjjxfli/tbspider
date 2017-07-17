# -*- coding: utf-8 -*-
#@author xfli
#@QQ 540331240
#@email lxf20054658@163.com

import sys
import threading
import time

import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
import logging
from scrapy.utils.log import configure_logging
import mysql.connector
from scrapy.exceptions import DropItem
from scrapy.exceptions import CloseSpider
from tbCrawlerUrlSpider.deps.urlHelper import urlHelper
from tbCrawlerUrlSpider.deps.urlItems import urlItems
from tbCrawlerUrlSpider.items import TbcrawlerurlspiderItem

from tbCrawlerUrlSpider.deps.tbUtils import *
from tbCrawlerUrlSpider import settings

reload(sys)
sys.setdefaultencoding('utf8')

class tbUrl(scrapy.Spider):
    name = "tbCrawlerUrlSpider"
    allowed_domains = ["taobao.com"]
    output_dir = settings.IMAGES_STORE

    start_urls = (
        'https://www.taobao.com',
    )
    pb_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36',
        'accept': '* / *',
        'accept - encoding': 'gzip, deflate, br',
        'accept - language': 'zh - CN, zh;q = 0.8'}

    def __get_next_id(self):
        if self.semaphore.acquire():
            self.id += 1
            self.semaphore.release()

    def __init__(self):
        self.id = 0
        self.urlHelper = urlHelper()
        self.semaphore = threading.Semaphore(2)
        # self.logger = logging.getLogger(self.name)
        log_file = ('%s/%s') % (settings.IMAGES_STORE, '/spider.log')
        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename=log_file,
            format='%(levelname)s: %(message)s',
            level=logging.DEBUG
        )
        dbargs = settings.DB_CONNECT
        db_server = settings.DB_SERVER
        conn = mysql.connector.connect(db_server, **dbargs)
        cursor = conn.cursor()
        cursor.execute('select max(id) from tb_urls_crawler where 1=1')
        values = cursor.fetchone()
        if values:
            self.id = values[0]
            self._read_db_data(cursor)
        cursor.close()
        conn.close()

    def _read_db_data(self,cursor):
        cur_line = 0
        page_count = 500
        next_line = cur_line + page_count

        while cur_line <= self.id:
            next_line = cur_line + page_count
            sql = ('select * from tb_urls_crawler limit %s,%s') % (cur_line, page_count)
            cursor.execute(sql)
            values = cursor.fetchall()
            cur_line = next_line
            if values:
                for v in values:
                    it = urlItems(None, v[2], None)
                    it.set_status(0)
                    it.set_depth(1)
                    self.urlHelper.append_url(it)
            else:
                break

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36',
                    'accept': '* / *',
                    'accept - encoding': 'gzip, deflate, br',
                    'accept - language': 'zh - CN, zh;q = 0.8'},
                # meta={'cur_url': url},
                args={'wait': 0.5})

    def parse(self, response):
        # 解析主题市场菜单
        site = Selector(response)
        parse_detail(settings.IMAGES_STORE,response)
        cats_list = site.xpath('//ul[@class="service-bd"]/li[@class="J_Cat a-all"]')

        for link in cats_list:
            url_list = link.xpath('.//span/a/@href').extract()
            cat_list = link.xpath('.//span/a/text()').extract()
            # print cat_list
            i = -1
            for url in url_list:
                url = get_formated_url(response, url)
                if url is None:
                    continue
                if self.urlHelper.is_url_visited(url):
                    print ('parse : url have been visited %s ') % (url)
                    continue
                i += 1
                cat = cat_list[i]
                it = urlItems(None, url, None)
                it.set_category(cat)
                it.set_status(0)
                it.set_depth(1)
                if not self.urlHelper.append_url(it):
                    return
                # cat = cat.decode('unicode_escape')
                url_item = TbcrawlerurlspiderItem()
                self.__get_next_id()
                url_item["id"] = self.id
                url_item["pid"] = 0
                url_item["url"] = url
                url_item["depth"] = 1
                url_item["max_depth"] = settings.MAX_VISIT_DEPTH
                url_item["create_time"] = time.time()
                logging.debug(url_item)
                yield url_item
                #item_list.append(url_item)

                if cat in settings.ALLOW_SPIDER_CATEGORY:
                    yield SplashRequest(
                        url,
                        self.parse_next,
                        headers=self.pb_headers,
                        meta={'item': it,'pid':self.id},
                        args={'wait': 0.5})

    '''
    解析类似*.taobao.com*的链接地址
    '''
    def parse_next(self,response):
        pre_it = response.meta["item"]
        pid = response.meta["pid"]
        site = Selector(response)
        urls_lists = site.xpath('//a/@href').extract()
        #更新old item
        pre_it.set_status(1)
        self.urlHelper.update_url(pre_it)

        if pre_it.get_depth() >= settings.MAX_VISIT_DEPTH:
            #raise DropItem("overflow: ")
            raise CloseSpider(reason='reach max depth')

        for u in urls_lists:
            url = get_formated_url(response,u)
            if url is None:
                continue

            if self.urlHelper.is_url_visited(url):
                print ('parse_next : url have been visited %s ') % (url)
                continue

            it = urlItems(pre_it.get_cur_url(), url, None)
            it.set_category(pre_it.get_cur_category())
            it.set_status(0)
            it.set_depth(pre_it.get_depth() + 1)
            if not self.urlHelper.append_url(it):
                continue

            url_item = TbcrawlerurlspiderItem()
            self.__get_next_id()
            url_item["id"] = self.id
            url_item["pid"] = pid
            url_item["url"] = url
            url_item["depth"] = pre_it.get_depth() + 1
            url_item["max_depth"] = settings.MAX_VISIT_DEPTH
            url_item["create_time"] = time.time()
            yield url_item
            #item_list.append(url_item)
            yield SplashRequest(
                url,
                self.parse_next,
                headers=self.pb_headers,
                meta={'item': it, 'pid': self.id},
                args={'wait': 0.5})

