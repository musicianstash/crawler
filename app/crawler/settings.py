# -*- coding: utf-8 -*-

# Scrapy settings for crawler project

DEBUG = True

BOT_NAME = 'crawler'

# Spiders location
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36')

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawler.pipelines.validate.ValidatePipeline': 400,
    'crawler.pipelines.dupefilter.DupeFilterPipeline': 401,
    'crawler.pipelines.send.SendPipeline': 500,
}

SEND_ITEM_JSON_RPC_HOST = 'http://eap:8080/apiv1/'

SEND_ITEM_JSON_RPC_METHOD = 'crawler.add_item'

# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    'crawler.middlewares.proxy.ProxyDownloaderMiddleware': 100,
    'crawler.middlewares.extensions.PyqueryDownloaderMiddleware': 543,
}

PROXIES = [
    'http://rgrabn:2VpbBYTg@23.81.240.205:29842'
]
