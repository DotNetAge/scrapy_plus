# -*- coding: utf-8 -*-

import pymongo
import logging

logger = logging.getLogger(__name__)


class MongoDBPipeline(object):
    """
    MongoDB数据管道
    
    配置方法：
    ITEM_PIPELINES = ['scrapyplus.pipelines.MongoDBPipeline', ]

    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "数据库名"
    MONGODB_COLLECTION = "表名"
    """

    def __init__(self, server=None, port=None, db_name=None, col=None):
        connection = pymongo.MongoClient(server, port)
        db = connection[db_name]
        self.collection = db[col]

    @classmethod
    def from_settings(cls, settings):
        server = settings['MONGODB_SERVER'],
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DB']
        collection_name = settings['MONGODB_COLLECTION']
        return cls(server, port, db_name, collection_name)

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        logger.debug("成功将数据插入至MongoDB",extra={'spider':spider})
        spider.crawler.stats.inc_value(
            'mongodb/inserted', spider=spider)
        return item
