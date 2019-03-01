# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import random


class ChromeMiddleware():
    """
    Chrome 无头浏览器仿真中间件。
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   exec_path=crawler.settings.get('CHROMEDRIVER'))

    def __init__(self, timeout=None, exec_path=''):
        self.logger = getLogger(__name__)  # 打开日志
        self.timeout = timeout
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # 采用无头浏览器
        self.browser = webdriver.Chrome(
            executable_path=exec_path, chrome_options=options)

        self.browser.set_window_size(1400, 700)  # 设置浏览窗口
        self.browser.set_page_load_timeout(self.timeout)  # 设置浏览器加载网页的超时时间
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()  # 释构时关闭浏览器实例

    def process_request(self, request, spider):
        """
        用Chrome抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug(u'启动Chrome...')
        # page = request.meta.get('sn', 1)

        try:
            self.browser.get(request.url)

            # 等待页面的宝贝全部加载完成
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.m-itemlist .items .item')))

            return HtmlResponse(url=request.url,
                                body=self.browser.page_source,
                                request=request,
                                encoding='utf-8',
                                status=200)

        except TimeoutException:
            # 超时抛出异常
            return HtmlResponse(url=request.url, status=500, request=request)

