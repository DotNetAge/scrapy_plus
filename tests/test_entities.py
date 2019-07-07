# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime

Base = declarative_base()


class Book(Base):
    """
    测试用的数据实体
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    alias = Column(String)
    summary = Column(Text)

