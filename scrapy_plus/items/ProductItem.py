# -*- coding: utf-8 -*-

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst
from scrapy_plus.processors import Text, CleanText, Price, Image, Url, Number


class ProductItem(Item):
    """
    商品实体
    """
    name = Field(input_processor=CleanText(),
                 output_processor=TakeFirst()),  # 品名
    link = Field(input_processor=Url(),
                 output_processor=TakeFirst())  # 链接地址
    image_urls = Field(input_processor=Image(),
                       output_processor=TakeFirst())  # 产品图片地址
    image_files = Field()  # 图片下载至本地的位置
    price = Field(input_processor=Price(),
                  output_processor=TakeFirst())  # 价格
    deal = Field(input_processor=Number(),
                 output_processor=TakeFirst())  # 成交人数
    free_shipping = Field(input_processor=CleanText(),
                          output_processor=TakeFirst())  # 是否包邮
    shop = Field(input_processor=CleanText(),
                 output_processor=TakeFirst())  # 淘宝店名
    location = Field(input_processor=CleanText(),
                     output_processor=TakeFirst())  # 地区
