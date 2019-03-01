# -*- coding: utf-8 -*-
import logging
from scrapy.utils.request import request_fingerprint
from redis import StrictRedis
from hashlib import md5
from scrapy.dupefilters import BaseDupeFilter


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class RedisBloomDupeFilter(BaseDupeFilter):

    def __init__(self, host='localhost', port=6379, db=0, blockNum=1, key='bloomfilter'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.redis = StrictRedis(host=host, port=port, db=db)

        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        _port = settings.getint('REDIS_PORT', 6379)
        _host = settings.get('REDIS_HOST', '127.0.0.1')
        _db = settings.get('REDIS_DB', 0)
        key = settings.get('BLOOMFILTER_REDIS_KEY', 'bloomfilter')
        block_number = settings.getint(
            'BLOOMFILTER_BLOCK_NUMBER', 1)

        return cls(_host, _port, _db, blockNum=block_number, key=key)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        if self.exists(fp):
            return True

        self.insert(fp)
        return False

    def exists(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str(str_input).encode('utf-8'))
        _input = m5.hexdigest()
        ret = True
        name = self.key + str(int(_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(_input)
            ret = ret & self.redis.getbit(name, loc)
        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str(str_input).encode('utf-8'))
        _input = m5.hexdigest()
        name = self.key + str(int(_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(_input)
            self.redis.setbit(name, loc, 1)

    def log(self, request, spider):
        msg = ("已过滤的重复请求: %(request)s")
        self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        spider.crawler.stats.inc_value(
            'redisbloomfilter/filtered', spider=spider)
