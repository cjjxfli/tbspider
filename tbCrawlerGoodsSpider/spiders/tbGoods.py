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
from scrapy.utils.log import configure_logging
import mysql.connector
from scrapy.exceptions import CloseSpider
from tbCrawlerGoodsSpider.items import TbcrawlergoodsspiderItem

from tbCrawlerUrlSpider.deps.tbUtils import *
from tbCrawlerUrlSpider import settings

reload(sys)
sys.setdefaultencoding('utf8')

class tbGoods(scrapy.Spider):
    name = "tbCrawlerGoodsSpider"
    allowed_domains = ["taobao.com"]
    output_dir = settings.IMAGES_STORE

    start_urls = (
    )
    pb_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36',
        'accept': '* / *',
        'accept - encoding': 'gzip, deflate, br',
        'accept - language': 'zh - CN, zh;q = 0.8'}

    def __init__(self):
        self.id = 0
        self.max_url_id = 0
        self.itmes = "item.taobao.com"
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
        goods_cursor = conn.cursor()
        goods_cursor.execute('select max(id) from tb_goods_crawler where 1=1')
        goods_value = goods_cursor.fetchone()
        if goods_value:
            self.id = goods_value[0]
        if self.id is None:
            self.id = 0
        cursor = conn.cursor()
        cursor.execute('select max(id) from tb_urls_crawler where 1=1')
        values = cursor.fetchone()
        if values:
            self.max_url_id = values[0]
            self._read_db_data(cursor)
        cursor.close()
        conn.close()

    def _read_db_data(self,cursor):
        cur_line = 0
        page_count = 500
        url_list = []

        while cur_line <= self.max_url_id:
            next_line = cur_line + page_count
            sql = ('select * from tb_urls_crawler where url like %s%s%s limit %s,%s') % ("'%",self.itmes,"%'",cur_line, page_count)
            cursor.execute(sql)
            values = cursor.fetchall()
            cur_line = next_line
            if values:
                for v in values:
                    url_list.append(v[2])
            else:
                break
        self.start_urls = tuple(url_list)

    def _get_next_id(self):
        if self.semaphore.acquire():
            self.id += 1
            self.semaphore.release()

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
        item_list = []
        print ('in parse_goods %s ') % (response.url)
        parse_detail(self.output_dir,response)
        it = TbcrawlergoodsspiderItem()
        self._get_next_id()
        it["id"] = self.id
        it["shop_name"] = ""
        it["shop_url"] = response.url
        it["shop_age"] = ""
        it["seller_name"] = ""
        it["goods_title"] = ""
        it["goods_url"] = response.url
        it["goods_commets_count"] = ""
        it["goods_sales_count"] = ""
        it["goods_img_url"] = ""
        it["goods_local_img_path"] = ""
        it["goods_old_price"] = ""
        it["goods_now_price"] = ""
        it["goods_details"] = ""
        it["create_time"] = time.time()

        site = Selector(response)
        shop_url = site.xpath('//div[contains(@class,"tb-shop-info-ft")]')
        shop_url = shop_url.xpath('.//a[0]/@href').extract()
        if len(shop_url) > 0:
            it["shop_url"] = shop_url[0]
        else:
            shop_url = site.xpath('//div[@class="header-operation"]/a[1]/@href').extract()
            if len(shop_url) > 0:
                it["shop_url"] = shop_url[0]
        goods_img_url = site.xpath('//span[contains(@class,"imagezoom")]/img/@src').extract()
        if len(goods_img_url) > 0:
            it["goods_img_url"] = goods_img_url[0]
        goods_details = site.xpath('//ul[@class="attributes-list"]/li/text()').extract()
        if len(goods_details) > 0:
            details = ""
            details = details.join(goods_details)
            it["goods_details"] = details
        # summary = site.xpath('//div[@class="tb-summary tb-clear"]')
        summary = site.xpath('//div[contains(@class,"tb-summary")]')
        # shop_name = sel.xpath('.//div[@class="tb-shop-name"]')
        shop_name = site.xpath('//div[contains(@class,"shop-name")]')
        shop_name = shop_name.xpath('.//a/text()')
        if len(shop_name) > 0:
            t = shop_name[0].extract()
            t = t.replace('\n', '', 2)
            t = t.lstrip()
            t = t.rstrip()
            it["shop_name"] = t
        else:
            shop_name = site.xpath('//span[contains(@class,"shop-name-title")]/text()').extract()
            if len(shop_name) > 0:
                t = shop_name[0]
                t = t.replace('\n', '', 2)
                t = t.lstrip()
                t = t.rstrip()
                it["shop_name"] = t
        # shop_seller = sel.xpath('.//div[@class="tb-shop-seller"]')
        shop_seller = site.xpath('//div[contains(@class,"shop-seller")]')
        shop_seller = shop_seller.xpath('.//a/text()')
        if len(shop_seller) > 0:
            t = shop_seller[0].extract()
            t = t.replace('\n', '', 2)
            t = t.lstrip()
            t = t.rstrip()
            it["seller_name"] = t
        else:
            shop_seller = site.xpath('//div[contains(@class,"shop-more-info")]/p[contains(@class,"info-item")][1]/text()').extract()
            if len(shop_seller) > 0:
                t = shop_seller[0]
                t = t.replace('\n', '', 2)
                t = t.lstrip()
                t = t.rstrip()
                it["seller_name"] = t
        shop_age = site.xpath('//span[@class="tb-shop-age-val"]').extract()
        if len(shop_age) > 0:
            it["shop_age"] = shop_age[0]

        for sel in summary:
            # title = sel.xpath('.//div[@class="tb-title"]')
            title = sel.xpath('.//div[contains(@class,"title")]')
            main_title = title.xpath('.//h3/text()').extract()
            sub_title = title.xpath('.//p/text()').extract()
            prices = sel.xpath('.//em[@class="tb-rmb-num"]/text()').extract()
            if len(prices) > 1:
                old_prices = prices[0]
                now_prices = prices[1]
                if len(old_prices) > 0:
                    t = old_prices
                    t = t.replace('\n', '', 2)
                    t = t.lstrip()
                    t = t.rstrip()
                    it["goods_old_price"] = t
            else:
                now_prices = prices[0]
            rate_counts = sel.xpath('.//div[@class="tb-rate-counter"]/a/strong/text()')
            seller_counts = sel.xpath('.//div[@class="tb-sell-counter"]/a/strong/text()')

            if len(main_title) > 0:
                t = main_title[0]
                t = t.replace('\n', '', 2)
                t = t.lstrip()
                t = t.rstrip()
                it["goods_title"] = t
            if len(sub_title) > 0:
                t = sub_title[0]
                t = t.replace('\n', '', 2)
                t = t.lstrip()
                t = t.rstrip()
                it["goods_title"] += t

            if len(now_prices) > 0:
                t = now_prices
                t = t.replace('\n', '', 2)
                t = t.lstrip()
                t = t.rstrip()
                it["goods_now_price"] = t
            if len(rate_counts) > 0:
                t = rate_counts[0].extract()
                t = t.replace('\n', '', 2)
                t = t.lstrip()
                t = t.rstrip()
                if (not t.isdigit()) and (not t.isnumeric()):
                    t = '0'
                it["goods_commets_count"] = t
            if len(seller_counts) > 0:
                t = seller_counts[0].extract()
                t = t.replace('\n', '', 2)
                t = t.lstrip()
                t = t.rstrip()
                if (not t.isdigit()) and (not t.isnumeric()):
                    t = '0'
                it["goods_sales_count"] = t
            item_list.append(it)
            if len(item_list) > 0:
                return item_list
            break
