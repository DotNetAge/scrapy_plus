# -*- coding: utf-8 -*-
from zope.interface import Interface, implementer
from scrapy.extensions.feedexport import IFeedStorage
from scrapy.exceptions import NotConfigured
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from importlib import import_module
from scrapy.exporters import BaseItemExporter
from logging import getLogger

logger = getLogger(__name__)


class EntityFileFaker():

    def __init__(self, session, entity_cls):
        self.session = session
        if entity_cls is None:
            raise NotConfigured

        self.entity_cls = entity_cls

    def write(self, keys, values):
        """
        将值写入到
        :param key: 实体的成员变量
        :param value: 实体字段值
        """
        entity = self.entity_cls()
        for key in keys:
            val = values.get(key)
            if val is not None:
                entity.__setattr__(key, val)
        self.session.add(entity)

    def close(self):
        self.session.commit()
        self.session.close()


@implementer(IFeedStorage)
class SQLFeedStorage():
    """
    SQL的存储后端
    @uri - SQL的连接字符串
    """

    @classmethod
    def from_crawler(cls, crawler, uri):
        return cls(uri,
                   crawler.settings.get('ORM_MODULE'),
                   crawler.settings.get('ORM_METABASE'),
                   crawler.settings.get('ORM_ENTITY'))

    def __init__(self, uri, mod_name=None, metabase_name=None, entity_name=None):
        """
        初始化SQL的存储后端
        FEED_URI 作为连接字符串使用
        """
        self.connection_str = uri
        self.mod_name = mod_name
        self.metabase = metabase_name
        self.entity_name = entity_name

    def open(self, spider):
        """
        通过连接字符串打开SQL数据库并返回生成的数据库上下文
        """
        engine = create_engine(self.connection_str)

        # 动态载入MetaData
        mod = import_module(self.mod_name)
        metabase = getattr(mod, self.metabase)
        entity_cls = getattr(mod, self.entity_name)
        metabase.metadata.bind = engine
        metabase.metadata.create_all()

        DBSession = sessionmaker(bind=engine)
        return EntityFileFaker(session=DBSession(), entity_cls=entity_cls)

    def store(self, file):
        """
        向数据提提交更改并关闭数据库
        """
        file.close()


class SQLItemExporter(BaseItemExporter):
    """
    将Item中的数据写入转换成为实体
    """

    def __init__(self, file, **kwargs):
        self.file = file
        self._configure(kwargs, dont_fail=True)

    def export_item(self, item):
        """
        将Item插入到数据库
        可以通过FEED_EXPORT_FIELDS设置要从Item中序列化至数据库的字段
        """

        self.file.write(self.fields_to_export if self.fields_to_export is not None and self.fields_to_export.__len__() else item.fields.keys(),
                        item)

        # TODO:要进行数据实体的转换就涉及数据类型转换问题，Item就需要进行序列化控制
