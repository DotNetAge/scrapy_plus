# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger


class HuabanMiddleware():

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   exec_path=crawler.settings.get('CHROMEDRIVER'),
                   username=crawler.settings.get('HUABAN_USR'),
                   password=crawler.settings.get('HUABAN_PWD'))

    def __init__(self, timeout=None, exec_path='', username='', password=''):
        self.logger = getLogger(__name__)  # 打开日志
        self.timeout = timeout
        self.usr = username
        self.pwd = password
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # 采用无头浏览器
        self.browser = webdriver.Chrome(executable_path=exec_path,
                                        options=options)

        self.browser.set_window_size(1400, 700)  # 设置浏览窗口
        self.browser.set_page_load_timeout(self.timeout)  # 设置浏览器加载网页的超时时间
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()  # 释构时关闭浏览器实例

    def login(self):

        login_button = self.browser.find_element_by_css_selector('.login.btn')
        login_button.click()
        form = self.browser.find_element_by_css_selector('form.mail-login')
        email_input = form.find_element_by_name('email')
        password_input = form.find_element_by_name('password')
        email_input.send_keys(self.usr)
        password_input.send_keys(self.pwd)
        form.submit()
        self._wait()

    def _wait(self):
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#index_footer')))

    def process_request(self, request, spider):
        """
        用Chrome抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug(u'启动Chrome...')

        try:
            self.browser.get(request.url)
            # 等待页脚被渲染完成
            self.browser.implicitly_wait(3)

            cookies = self.browser.get_cookies()
            is_login = False
            for cookie in cookies:
                if cookie['name'] == 'sid':
                    is_login = True
                    break

            if not is_login:
                self.login()
                self.browser.get(request.url)
                self.browser.implicitly_wait(3)

            return HtmlResponse(url=request.url,
                                body=self.browser.page_source,
                                request=request,
                                encoding='utf-8',
                                status=200)

        except TimeoutException:
            # 超时抛出异常
            return HtmlResponse(url=request.url, status=500, request=request)
