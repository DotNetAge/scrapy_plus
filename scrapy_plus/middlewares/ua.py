# -*- coding: utf-8 -*-

import random


class RandomUserAgentMiddleware(object):
    """
    随机User Agent 中间件
    """
    @classmethod
    def from_crawler(cls, crawler):
        return cls(user_agents=crawler.settings.getlist('USER_AGENTS'))

    def __init__(self, user_agents=[]):
        self.user_agents = user_agents

    def process_request(self, request, spider):
        if self.user_agents != None and len(self.user_agents) > 0:
            request.headers.setdefault(
                b'User-Agent', random.choice(self.user_agents))
