# -*- coding: utf-8 -*-
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose, Compose, Identity, Join
from w3lib.html import remove_tags


class NewsItem(Item):
    title = Field(output_processor=TakeFirst())
    desc = Field(input_processor=MapCompose(str.strip,
                                            stop_on_none=True),
                 output_processor=TakeFirst())
    link = Field(output_processor=TakeFirst())
    pub_date = Field(input_processor=MapCompose(lambda v: v.split()[0],
                                                stop_on_none=True),
                     output_processor=TakeFirst())
    body = Field(input_processor=MapCompose(remove_tags, str.strip,
                                            stop_on_none=True),
                 output_processor=TakeFirst())
