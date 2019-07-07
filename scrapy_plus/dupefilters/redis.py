# -*- coding: utf-8 -*-
import logging
from redis import Redis
from scrapy.dupefilters import BaseDupeFilter



class RedisDupeFilter(BaseDupeFilter):
    """
    Redis 去重过滤器
    """
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = Redis(host=host, port=port, db=db)
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', 'localhost')
        redis_port = settings.getint('REDIS_PORT')
        redis_db = settings.get('REDIS_DUP_DB')
        return cls(host, redis_port, redis_db)

    def request_seen(self, request):
        fp = request.url
        key = 'UrlFingerprints'
        if not self.redis.sismember(key, fp):
            self.redis.sadd(key, fp)
            return False
        return True

    def log(self, request, spider):
        msg = ("已过滤的重复请求: %(request)s")
        self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)


