# -*- coding: utf-8 -*-
"""
洋葱头代理
"""
# from scrapy import signals
from logging import getLogger
from stem.control import Controller
import stem
# import random
import time

logger = getLogger(__name__)

class TorProxyMiddleware(object):
    """
    洋葱头代理中间件

    ## settings.py 中的配置说明

    - HTTP_PROXY - 本机的代理端口
    - TOR_CTRL_PORT - 本机Tor的控制端口
    - TOR_PASSWORD - 登入Tor的密码
    """

    def __init__(self, tor_proxy='127.0.0.1:8118', tor_control_port=9051, tor_password=None, after_times=50):

        if not tor_proxy:
            raise Exception('http proxy setting should not be empty')

        if not tor_control_port:
            raise Exception('tor control port setting should not be empty')

        if not tor_password:
            raise Exception('tor password setting should not be empty')

        self.http_proxy = tor_proxy
        self.tor_control_port = tor_control_port
        self.tor_password = tor_password
        self.count = 0
        self.times = after_times

    @classmethod
    def from_crawler(cls, crawler):
        tor_proxy = crawler.settings.get('TOR_PROXY')
        tor_control_port = crawler.settings.getint('TOR_CTRL_PORT')  # 默认为9051
        tor_password = crawler.settings.get('TOR_PASSWORD')
        after_times = crawler.settings.get('TOR_CHANGE_AFTER_TIMES')
        return cls(tor_proxy, tor_control_port, tor_password, after_times)

    def process_request(self, request, spider):
        # 当启用Retry中间件，并且曾经出现2次的Retry就应该尝试更换IP
        retry_times = request.meta.get('retry_times', 0)

        if (self.count > 0 and self.count % self.times == 0) or retry_times>= 2:
            logger.debug("正在更换新的IP地址")
            self.ip_renew(spider)

        self.count += 1

        request.meta['proxy'] = self.http_proxy

    def ip_renew(self,spider):
        """access tor ControlPort to signal tor get a new IP
        """
        with Controller.from_port(port=self.tor_control_port) as controller:
            controller.authenticate(password=self.tor_password)
            controller.signal(stem.Signal.NEWNYM)
            time.sleep(controller.get_newnym_wait())
            controller.close()
            spider.crawler.stats.inc_value('renew_ip/count')
