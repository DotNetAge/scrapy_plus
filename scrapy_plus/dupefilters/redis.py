# -*- coding: utf-8 -*-
import logging
from scrapy.utils.request import request_fingerprint
from redis import StrictRedis
from scrapy.dupefilters import BaseDupeFilter

BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 30


class RedisDupeFilter(BaseDupeFilter):
    """
    Redis去重过滤器
    """

    @classmethod
    def from_settings(cls, settings):
        return cls(host=settings.get('REDIS_HOST'),
                   port=settings.getint('REDIS_PORT'),
                   db=settings.get('REDIS_DB'))

    def __init__(self, host, port, db):
        self.redis = StrictRedis(host=host, port=port, db=db)
        self.logger = logging.getLogger(__name__)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        key = 'UriFingerprints'
        if self.redis.sismember(key, fp) is None:
            self.redis.sadd(key, fp)
            return False
        return True

    def log(self, request, spider):
        msg = ("已过滤的重复请求:%(request)s")
        self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
