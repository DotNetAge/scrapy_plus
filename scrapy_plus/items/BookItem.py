# coding:utf-8

from scrapy import Item, Field
from ..processors import Number, Date, Price, Text, CleanText
from scrapy.loader.processors import TakeFirst, Join


class BookItem(Item):
    # 书名
    name = Field(input_processor=CleanText(),
                 output_processor=TakeFirst())
    # 作者
    authors = Field(input_processor=CleanText(),
                    output_processor=TakeFirst())
    # 出版社
    publishing_house = Field(input_processor=CleanText(),
                             output_processor=TakeFirst())
    # 出品方
    publisher = Field(input_processor=CleanText(),
                      output_processor=TakeFirst())
    # 原名
    origin_name = Field(input_processor=CleanText(),
                        output_processor=TakeFirst())
    # 译者
    translators = Field(input_processor=CleanText(),
                        output_processor=TakeFirst())
    # 出版时间
    pub_date = Field(input_processor=Date(),
                     output_processor=TakeFirst())
    # 页数
    pages = Field(input_processor=Number(),
                  output_processor=TakeFirst())
    # 定价
    price = Field(input_processor=Price(),
                  output_processor=TakeFirst())
    # ISBN
    isbn = Field(input_processor=CleanText(),
                 output_processor=TakeFirst())
    # 豆瓣评分
    rates = Field(input_processor=Number(),
                  output_processor=TakeFirst())
    # 评价数
    rating_count = Field(input_processor=Number(),
                         output_processor=TakeFirst())
    # 简介
    summary = Field(input_processor=Text(),
                    output_processor=Join())
    # 作者简介
    about_authors = Field(input_processor=CleanText(),
                          output_processor=TakeFirst())
