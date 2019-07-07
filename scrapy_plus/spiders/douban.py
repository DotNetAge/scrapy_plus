# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..items import BookItem


class BookSpider(CrawlSpider):
    name = "doubanbook"
    start_urls = ['https://book.douban.com/tag/']
    rules = (Rule(LinkExtractor(allow=('\/tag\/(.*?)')), follow=True),
             Rule(LinkExtractor(allow=('\/tag\/(.*?)\?start\='),
                                tags=('link'), attrs=('href')), follow=True),
             Rule(LinkExtractor(allow=('\/subject\/.*'), ), follow=False, callback='parse_item'))

    def parse_item(self, response):
        loader = ItemLoader(item=BookItem(), response=response)
        loader.add_css('name',"h1 span::text") # 标题
        loader.add_css('summary','.related_info #link-report .intro p::text') # 简介
        loader.add_xpath('authors', u'//span[.//text()[normalize-space(.)="作者:"]]/following::text()[1]')
        loader.add_xpath('authors', u'//span[.//text()[normalize-space(.)="作者:"]]/following::text()[2]')
        loader.add_xpath('publishing_house', u'//span[.//text()[normalize-space(.)="出版社:"]]/following::text()[1]')
        loader.add_xpath('publisher', u'//span[.//text()[normalize-space(.)="出品方:"]]/following::text()[1]')
        loader.add_xpath('publisher', u'//span[.//text()[normalize-space(.)="出品方:"]]/following::text()[2]')
        loader.add_xpath('origin_name', u'//span[.//text()[normalize-space(.)="原作名:"]]/following::text()[1]')
        loader.add_xpath('translators', u'//span[.//text()[normalize-space(.)="译者:"]]/following::text()[1]')
        loader.add_xpath('translators', u'//span[.//text()[normalize-space(.)="译者"]]/following::text()[2]')
        loader.add_xpath('pub_date', u'//span[.//text()[normalize-space(.)="出版年:"]]/following::text()[1]')
        loader.add_xpath('pages', u'//span[.//text()[normalize-space(.)="页数:"]]/following::text()[1]')
        loader.add_xpath('price', u'//span[.//text()[normalize-space(.)="定价:"]]/following::text()[1]')
        loader.add_xpath('isbn', u'//span[.//text()[normalize-space(.)="ISBN:"]]/following::text()[1]')
        loader.add_css('rates',".rating_num::text") # 得分
        loader.add_css('rating_count', ".rating_people>span::text") #投票
        return loader.load_item()

