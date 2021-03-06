# -*- coding: utf-8 -*-

# Scrapy settings for tbCrawlerUrlSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tbCrawlerUrlSpider'

SPIDER_MODULES = ['tbCrawlerUrlSpider.spiders']
NEWSPIDER_MODULE = 'tbCrawlerUrlSpider.spiders'

IMAGES_STORE = 'h:/myprojects/Python/shop/tbCrawlerUrlSpider/data/taobao'
SPLASH_URL = 'http://192.168.137.130:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobaospider (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3135.4 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ALLOW_SPIDER_CATEGORY = ['女装','男装','内衣','鞋靴','箱包','配件','童装','玩具','孕产','美妆','洗护','保健品']
#每个品类最大抓取条目
MAX_SPIDER_COUNT = 2000
#最多重复N次访问，超过则停止爬取
MAX_REVISIT_TRY = 100000
#禁止重试
#RETRY_ENABLED = False
#关闭重定向
REDIRECT_ENABLED = False
#设置下载超时
#DOWNLOAD_TIMEOUT = 15
#防止被屏蔽
COOKIES_ENABLED=False
#最大访问深度
MAX_VISIT_DEPTH=3

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'taobaospider.middlewares.MyCustomDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    # Engine side
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # Downloader side
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'tbCrawlerUrlSpider.pipelines.TbcrawlerurlspiderPipeline': 300,
    'tbCrawlerUrlSpider.pipelines.MySQLStoreTbUrlPipeline': 350,
}
DOWNLOAD_DELAY = 3

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

DB_SERVER = 'MySQLdb'
DB_CONNECT = {
    'host':'localhost',
    'user':'root',
    'passwd':'123456',
    'port':3306,
    'db':'tb_url',
    'charset':'utf8',
    'use_unicode':True
}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tbCrawlerUrlSpider.middlewares.TbcrawlerurlspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tbCrawlerUrlSpider.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'tbCrawlerUrlSpider.pipelines.TbcrawlerurlspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
