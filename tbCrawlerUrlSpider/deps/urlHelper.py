# -*- coding: utf-8 -*-
#@author xfli
#@QQ 540331240
#@email lxf20054658@163.com
from tbCrawlerUrlSpider.deps.urlItems import urlItems

class urlHelper(object):
    '''
    以urlItems中的cur_url为key，列表为value
    如：{'https://www.taobao.com/markets/nvzhuang/taobaonvzhuang':[it1]}
    '''
    __url_depth_1 = {}
    __url_depth_2 = {}
    __url_depth_3 = {}

    '''
    判断给定url是否已经抓取过
    1.判断__url_depth_1是否存在
    2.判断__url_depth_2是否存在
    3.判断__url_depth_3是否存在
    '''
    def is_url_visited(self,url):
        if url is None:
            print 'url is illegal'
            return True
        if self.__url_depth_1.has_key(url):
            return True
        if self.__url_depth_2.has_key(url):
            return True
        if self.__url_depth_3.has_key(url):
            return True
        return False

    def is_url_in_dict_1(self,url):
        if self.__url_depth_1.has_key(url):
            return True
        return False

    def is_url_in_dict_2(self,url):
        if self.__url_depth_2.has_key(url):
            return True
        return False

    def is_url_in_dict_3(self,url):
        if self.__url_depth_3.has_key(url):
            return True
        return False

    '''
    添加一个item到列表，根据item的depth插入到对应的列表
    '''
    def append_url(self,item):
        if not isinstance(item, urlItems):
            return False
        url = item.get_cur_url()
        if self.is_url_visited(url):
            return True
        dp = item.get_depth()
        if dp <= 1:
            self.__url_depth_1[url] = item
        elif dp == 2:
            self.__url_depth_2[url] = item
        elif dp == 3:
            self.__url_depth_3[url] = item
        else:
            print 'illegal item'
            return False
        return True

    def __update_url(self,old_item,item):
        if not isinstance(old_item, urlItems) or (not isinstance(item, urlItems)):
            return False
        old_item.set_pre_url(item.get_pre_url())
        old_item.set_after_url(item.get_after_url())
        old_item.set_category(item.get_cur_category())
        old_item.set_status(item.get_status())
        old_item.set_depth(item.get_depth)
        return True

    '''
    更新item指定的数据
    '''
    def update_url(self,item):
        if not isinstance(item, urlItems):
            return False
        url = item.get_cur_url()
        if not self.is_url_visited(url):
            return False
        if self.is_url_in_dict_1(url):
            old_item = self.__url_depth_1[url]
            self.__update_url(old_item,item)
        elif self.is_url_in_dict_2(url):
            old_item = self.__url_depth_2[url]
            self.__update_url(old_item,item)
        elif self.is_url_in_dict_3(url):
            old_item = self.__url_depth_3[url]
            self.__update_url(old_item,item)
        else:
            return False
        return True

    '''
    打印url报表
    '''
    def output_reports(self):
        pass