# -*- coding: utf-8 -*-
import os
from scrapy import log
import logging
from scrapy.utils.response import get_base_url

def parse_detail(output_dir, response):
    outputfile = _rtouch(output_dir,response.url)
    if not outputfile:
        msg = ('download file: %s') % (response.url)
        logging.getLogger('tbCrawlerUrlSpider').log(msg, level=log.WARNING)
        return
    try:
        with open(outputfile, 'w') as f:
            f.write(response.body)
            msg = ('download file: %s') % (outputfile)
            logging.info(msg)
    except:
        print 'open file failed'
        return
    else:
        f.close()


def _rtouch(output_dir,filepath):
    pos = filepath.find('://')
    file_name = "index.html"
    if -1 != pos:
        filepath = filepath[pos + 3:]
    pos = filepath.rfind('/')
    if -1 != pos:
        file_name = filepath[pos:]
        filepath = filepath[0:pos]
        # 取10个字符作为文件名
        file_name = file_name[-10:]

    filepath += "/" + file_name + ".html"
    opath = os.path.abspath(output_dir + "/" + filepath)
    basedir = os.path.dirname(opath)
    if not os.path.exists(basedir):
        try:
            os.makedirs(basedir)
        except Exception, msg:
            logging.getLogger('tbCrawlerUrlSpider').log(msg, level=log.WARNING)
            return None
    return opath


def strcmp( str1, str2):
    i = 0
    while i < len(str1) and i < len(str2):
        outcome = cmp(str1[i], str2[i])
        if outcome:
            return outcome
        i += 1
    return cmp(len(str1), len(str2))


def get_formated_url(res, url):
    base_url = get_base_url(res)
    protocol = 'https'
    pos = base_url.find('://')
    if -1 != pos:
        protocol = base_url[:pos]
    t = url
    t = t.split('.')
    if len(t) < 2:
        return None
    if (not 'taobao' in t) and (not 'com' in t):
        print ('get_formated_url %s ') % (url)
        return None
    t = url
    pos = t.find('//')
    if -1 != pos and pos <= 1:
        t = t[pos + 2:]
        full_url = ('%s://%s') % (protocol, t)
        return full_url
    return url


def is_item(url):
    t = url.split('://')
    try:
        t = t[1]
        t = t.split('.')
        if strcmp(t[0], 'item') == 0:
            return True
        return False
    except:
        print 'error'
    return False
