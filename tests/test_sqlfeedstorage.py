# -*- coding: utf-8 -*-

import unittest
from scrapy_plus.extensions import SQLFeedStorage
from scrapy_plus.extensions.sql import EntityFileFaker

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


class SQLFeedStorageTestCase(unittest.TestCase):
    """
    SQLFeedStorage单元测试
    """

    def setUp(self):
        self.book = {
            'id': 1,
            'name': "Vue2实践揭秘",
            'alias': "Vue2实践揭秘 - 电子工业出版社出版",
            'summary': "这是一本关于Vue2实践的书籍，由浅入深层层揭显Vue2中的隐秘。"
        }

        self.connection_str = "sqlite:///test.db"

    def test_entity_faker_should_banch_update(self):
        from tests.test_entities import Base, Book

        engine = create_engine(self.connection_str)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)

        Base.metadata.create_all()
        faker = EntityFileFaker(DBSession(), Book)

        faker.write(self.book.keys(), self.book)
        faker.close()

        session = DBSession()
        books = session.query(Book).all()
        self.assertEqual(books.__len__(), 1)
        faker.close()

        Base.metadata.drop_all()

    def test_sql_feed_storage_should_create_database(self):
        storage = SQLFeedStorage('sqlite:///test1.db',
                                 'tests.test_entities', 'Base', 'Book')
        file = storage.open(None)
        file.write(self.book.keys(), self.book)
        storage.store(file)


if __name__ == '__main__':
    unittest.main()
