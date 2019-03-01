# -*- coding: utf-8 -*-

import random


class RandomProxyMiddleware(object):
    """
    随机代理。在运行时会从settings.py设置的PROXIES中随机抽取一个作为当前代理地址。
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(proxies=crawler.settings.getlist('HTTP_PROXIES'))

    def __init__(self, proxies=[]):
        self.proxies = proxies

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxies)
