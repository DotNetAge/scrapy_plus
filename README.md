# Scrapy+

Scrapy扩展工具包。具体使用方法与配置方法可以参考《虫术——Python绝技》一书。

## 过滤器

### Redis 去重过滤器 `scrapy_plus.dupefilters.RedisDupeFilter`

基于Redis使用`Set`存储曾访问过的URL。

**使用方法**

在`settings`文件内引入以下的内容:

```py
# 覆盖原有的去重过滤器
DUPEFILTER_CLASS = 'scrapy_plus.dupefilters.RedisDupeFilter' 
REDIS_PORT = 6379                       # REDIS服务器端口
REDIS_HOST = '127.0.0.1'                # REDIS服务器地址
REDIS_DB = 0                            # 数据库名
```

**默认配置**

```py
REDIS_PORT = 6379                       # REDIS服务器端口
REDIS_HOST = '127.0.0.1'                # REDIS服务器地址
REDIS_DB = 0                            # 数据库名
```

### Redis 布隆去重过滤器 `scrapy_plus.dupefilters.RedisBloomDupeFilter`

基于Redis采用布隆算法对URL进行去重处理

**使用方法**

在`settings`文件内引入以下的内容:

```py
# 覆盖原有的去重过滤器
DUPEFILTER_CLASS = 'scrapy_plus.dupefilters.RedisBloomDupeFilter' 
REDIS_PORT = 6379                       # REDIS服务器端口
REDIS_HOST = '127.0.0.1'                # REDIS服务器地址
REDIS_DB = 0                            # 数据库名
```

**默认配置**

```
REDIS_PORT = 6379                       # REDIS服务器端口
REDIS_HOST = '127.0.0.1'                # REDIS服务器地址
REDIS_DB = 0                            # 数据库名
BLOOMFILTER_REDIS_KEY = 'bloomfilter'   # 去重键名
BLOOMFILTER_BLOCK_NUMBER = 1            # 块大小
```

## 中间件

### 自登录中间件 `scrapy_plus.middlewares.LoginMiddleWare`

```py
LOGIN_URL = '网站登录地址'
LOGIN_USR = '用户名'
LOGIN_PWD = '密码'
LOGIN_USR_ELE = '用户名input元素名称(name)'
LOGIN_PWD_ELE = '密码input元素名称(name)'
DOWNLOADER_MIDDLEWARES = {
    'scrapyplus.middlewares.LoginMiddleWare': 330
}
```

### Chrome 浏览器仿真中间件 `scrapy_plus.middlewares.ChromeMiddleware`

Chrome 无头浏览器仿真中间件。让爬虫用Chrome来访问目标URL，完美解决富JS页面的问题。

```py
SELENIUM_TIMEOUT = 30 # 设置页面打开的超时秒数
CHROMEDRIVER = "/path/to/chrome" # Chrome浏览器驱动地址
DOWNLOADER_MIDDLEWARES = {
    'scrapyplus.middlewares.ChromeMiddleware': 800
}

```


### Splash `scrapy_plus.middlewares.SplashSpiderMiddleware`

Splash 中间件，可将请求转发至指定的Splash服务，使蜘蛛具有浏览器仿真功能。

```py
WAIT_FOR_ELEMENT = "选择器" # 等待该元素被加载成功才认为页面加载完成
DOWNLOADER_MIDDLEWARES = {
    'scrapyplus.middlewares.SplashSpiderMiddleware': 800
}
```

### 随机UA `scrapyplus.middlewares.RandomUserAgentMiddleware`

随机模拟User Agent

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapyplus.middlewares.RandomUserAgentMiddleware': 500
}
## 可随机增加更多的UA，中间件会进行自动随机选择
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.83 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
]
```

### Tor 中间件 `scrapyplus.middlewares.TorProxyMiddleware`

洋葱头代理中间件,让你的蜘蛛不停地更换IP地址,化身万千。

需要先安装 tor 与 privoxy 具体配置方法请参考《虫术——python绝技》

```py
# Tor代理
TOR_PROXY = 'http://127.0.0.1:8118'  # 8118是Privoxy的默认代理端口
TOR_CTRL_PORT = 9051
TOR_PASSWORD = 'mypassword'
TOR_CHANGE_AFTER_TIMES = 50 # 在发出多少次请求之后更换IP地址。
```

## 管道

### MongoDB数据存储管道 `scrapy_plus.piplines.MongoDBPipeline`

可以将Item直接写入MongoDB数据库中。

**默认配置**

```py
ITEM_PIPELINES = {'scrapy_plus.pipelines.MongoDBPipeline':2}

MONGODB_SERVER = "localhost"    # mongodb服务器地址
MONGODB_PORT = 27017            # mongodb服务端口
MONGODB_DB = "数据库名"          # 数据库名
MONGODB_COLLECTION = "表名"     # 表名
```

## 存储后端

### SQL数据库存储后端 `scrapy_plus.extensions.SQLFeedStorage`

```py
# 数据存储
ORM_MODULE = 'movies.entities'
ORM_METABASE = 'Base'
ORM_ENTITY = 'Movie'

FEED_FORMAT = 'entity' # 
FEED_EXPORTERS = {
    'entity': 'scrapyplus.extensions.SQLItemExporter'
}

FEED_URI = 'dialect+driver://username:password@host:port/database'  # 默认后端存储文件的名称
FEED_STORAGES = {
    'sqlite': 'scrapyplus.extensions.SQLFeedStorage',
    'postgresql': 'scrapyplus.extensions.SQLFeedStorage',
    'mysql': 'scrapyplus.extensions.SQLFeedStorage'
}
```

### 阿里云OSS存储后端 `scrapy_plus.extensions.OSSFeedStorage`

```py
OSS_ACCESS_KEY_ID = ''
OSS_SECRET_ACCESS_KEY = ''
```