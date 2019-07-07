# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse, FormRequest
from logging import getLogger


class LoginMiddleWare():
    """
    预登录表单中间件
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(login_url=crawler.settings.get('LOGIN_URL'),
                   user_name=crawler.settings.get('LOGIN_USR'),
                   password=crawler.settings.get('LOGIN_PWD'),
                   user_ele=crawler.settings.get('LOGIN_USR_FIELD'),
                   pwd_ele=crawler.settings.get('LOGIN_PWD_FIELD'))

    def __init__(self, login_url, user_name, password, user_ele='username', pwd_ele='password'):
        self.logger = getLogger(__name__)  # 打开日志
        self.login_url = login_url
        self.user_name = user_name
        self.password = password
        self.user_ele = user_ele
        self.pwd_ele = pwd_ele

    def process_request(self, request, spider):
        cookies = request.headers.getlist('Cookie')
        if cookies is None or len(cookies)==0:
            return FormRequest(url=self.login_url,
                               formdata={self.user_ele: self.user_name, self.pwd_ele: self.password})
        return request

    def process_response(self, request, response, spider):
        if "authentication failed" in response.body:
            return IgnoreRequest()

    def process_exception(self, request, exception, spider):
        self.logger.error("登录失败")
