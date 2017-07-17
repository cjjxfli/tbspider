# -*- coding: utf-8 -*-
#@author xfli
#@QQ 540331240
#@email lxf20054658@163.com

from tbCrawlerUrlSpider import settings
from tbCrawlerUrlSpider.deps.tbUtils import *

'''
表示一个url的状态，url的前继，后继，深度，状态
status为0时表示初始状态，为1时表示url抓取成功，为2时表示url抓取失败
'''

class urlItems(object):
    pre_url = None
    cur_url = None
    after_url = None
    url_category = None
    status = 0
    depths = 0

    def __init__(self,pre,cur,after):
        self.set_pre_url(pre)
        self.set_cur_url(cur)
        self.set_after_url(after)

    def set_pre_url(self,url):
        if not (url is None):
            self.pre_url = url

    def set_cur_url(self,url):
        if not (url is None):
            self.cur_url = url

    def set_after_url(self,url):
        if not (url is None):
            self.after_url = url

    def set_category(self,cat):
        if not (cat is None):
            self.url_category = cat

    def set_status(self,st):
        if isinstance(st,int) and st <= 2:
            self.status = st

    def set_depth(self,dp):
        if isinstance(dp,int) and dp <= settings.MAX_VISIT_DEPTH:
            self.depths = dp

    def get_pre_url(self):
        return self.pre_url

    def get_cur_url(self):
        return self.cur_url

    def get_after_url(self):
        return self.after_url

    def get_cur_category(self):
        return self.url_category

    def get_status(self):
        return self.status

    def get_depth(self):
        return self.depths

