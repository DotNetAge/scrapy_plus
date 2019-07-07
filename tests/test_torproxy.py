# -*- coding: utf-8 -*-

import unittest
from scrapy_plus.middlewares.tor import TorProxyMiddleware
from scrapy.http import Request
from urllib3 import ProxyManager


class TorProxyMiddlewareTestCase(unittest.TestCase):

    def test_tor_should_change_diff_ips(self):
        tor = TorProxyMiddleware(tor_proxy='127.0.0.1:8118',
                                 tor_password='mypassword',
                                 after_times=2)
        request = Request(url='http://www.baidu.com')
        ip = self.get_ip()
        for i in range(1, 10):
            tor.process_request(request, None)
            if i > 1 and (i % 2) != 0:
                new_ip = self.get_ip()
                self.assertNotEqual(ip, new_ip)
                ip = new_ip

    def get_ip(self):
        http = ProxyManager('http://127.0.0.1:8118')
        body = http.request('GET', 'http://icanhazip.com')
        return str(body.data, 'utf-8').replace('\n', '')


if __name__ == '__main__':
    unittest.main()
