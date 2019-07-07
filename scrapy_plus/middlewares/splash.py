# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy_splash import SplashRequest

class SplashSpiderMiddleware():
    """
    Splash 中间件，可将请求转发至指定的Splash服务，使蜘蛛具有浏览器仿真功能。
    """
    # 以下的Lua脚本会生一个等待指定元素选择器加载完成的函数
    lua_source = """
         function wait_for_element(splash, css, maxwait)
           -- Wait until a selector matches an element
           -- in the page. Return an error if waited more
           -- than maxwait seconds.
           if maxwait == nil then
               maxwait = 10
           end
           return splash:wait_for_resume(string.format([[
             function main(splash) {
               var selector = '%s';
               var maxwait = %s;
               var end = Date.now() + maxwait*1000;

               function check() {
                 if(document.querySelector(selector)) {
                   splash.resume('Element found');
                 } else if(Date.now() >= end) {
                   var err = 'Timeout waiting for element';
                   splash.error(err + " " + selector);
                 } else {
                   setTimeout(check, 200);
                 }
               }
               check();
             }
           ]], css, maxwait))
     end

    function main(splash, args)
       splash:go(args.url)
       wait_for_element(splash, args.wait_for_element)
       return splash:html()
    end
 """

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(wait_for_element=crawler.settings.get('WAIT_FOR_ELEMENT'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self, wait_for_element=None):
        self.wait_for_element = wait_for_element

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for request in start_requests:
            yield SplashRequest(request.url,
                                request.callback,
                                endpoint='execute',
                                meta=dict(request.meta),
                                args={
                                    'lua_source': self.lua_source,
                                    'wait_for_element': self.wait_for_element,
                                    'wait': 3}
                                )

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
