# Scrapy+

Scrapy扩展工具包。为[《从0学爬虫专栏》](https://www.imooc.com/read/34) 提供，详细的使用方法请到专栏内参考。

```
$ pip install scrapy_plus
```

Scrapy+提供以下的内容

- 过滤器
  - Redis 去重过滤器
  - Redis 布隆去重过滤器
- 中间件
  - 自登录中间件
  - 花瓣网专用中间件
  - Chrome通用中间件
  - Splash渲染中间件
  - Tor中间件
  - 随机UA中间件
  - 随机代理中间件
- 管道
  - MongoDB数据存储管道
  - 可支持阿里云的OSS图片管道
- SQL存储端
- 输入/输出处理器
- 蜘蛛
  - `BookSpider`
  - `NeteaseSpider`
  - `TaobaoSpider`