# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import NewsItem
from scrapy.loader import ItemLoader


class NeteaseSpider(CrawlSpider):
    name = 'netease'
    allowed_domains = ['163.com']
    urls = 'https://www.163.com/'
    start_urls = urls.split(',')

    rules = (
        Rule(LinkExtractor(allow=r'(\w+):\/\/([^/:]+)\/(\d{2})+\/(\d{4})+\/(\d{2})+\/([^#]*)'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=NewsItem(), response=response)
        loader.add_css('title', '#epContentLeft>h1::text')
        loader.add_css('pub_date', '#epContentLeft .post_time_source::text')
        loader.add_css('desc', '#epContentLeft .post_desc::text')

        # 游戏栏目 play.163.com
        loader.add_css('title', 'h1.article-h1::text')
        loader.add_css('desc', '.artical-summary::text')

        # 人间栏目 renjian.163.com
        loader.add_css('title', '.bannertext>.daxie_sub_title::text')
        loader.add_css('pub_date', '.sub_title>.pub_time::text')

        # 体育 sports.163.com
        loader.add_css('title', '.m-article .article-top>.article-title::text')
        loader.add_xpath('body', '//div[@class=".article-details"]')

        loader.add_xpath('body', '//div[@id="endText"]')
        loader.add_value('link', response.url)
        return loader.load_item()
