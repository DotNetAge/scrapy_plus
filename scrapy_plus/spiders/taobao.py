# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import urllib
from ..items import ProductItem
from scrapy.loader import ItemLoader


class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['s.taobao.com']
    base_url = 'https://s.taobao.com/search?q=%s'

    def start_requests(self):
        keywords = self.gen_keywords()

        for kw in keywords:
            url = self.base_url % urllib.parse.quote(kw.encode('utf-8'))
            yield Request(url, self.parse, meta={'kw': kw})

    def gen_keywords(self):
        raise NotImplemented

    def parse(self, response):

        products = response.css('#mainsrp-itemlist .items .item')

        for product in products:
            loader = ItemLoader(item=ProductItem(), selector=product)
            loader.add_css('price', '.price>strong::text')
            loader.add_css('name', 'div.title>a::text')
            loader.add_css('shop', '.shopname>span::text')
            loader.add_css('image_url', '.pic img::attr(data-src)')
            loader.add_css('deal', '.deal-cnt::text')
            loader.add_css('location', '.location::text')
            loader.add_css('link', 'div.title>a::attr(href)')
            loader.add_css('free_shipping', '.icon-service-free')

            yield loader.load_item()
