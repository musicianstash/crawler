# -*- coding: utf-8 -*-

from ftfy import fix_text

from pyquery import PyQuery
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from crawler.contrib.spiders.mixins.modular import ModularMixin
from crawler.items import MusicGearItem
from crawler.contrib import format

DENY_LINKS = ['brands', 'airplanes', 'other']


class MusiciansFriendSpider(ModularMixin, CrawlSpider):
    name = 'onedrone.com'
    allowed_domains = ['onedrone.com', 'hobbytron.com']
    item = MusicGearItem

    spider_store = 'OneDrone'
    spider_currency = 'EUR'
    spider_countries = ['*']

    download_delay = 5

    start_urls = ['http://www.onedrone.com/store/']

    rules = (
        Rule(LinkExtractor(restrict_css='.main-navigation > li', deny=DENY_LINKS,
                           tags=['span'], attrs=['data-url'])),
        Rule(LinkExtractor(restrict_css='.pagination')),
        Rule(LinkExtractor(restrict_css='.product-thumb'), callback='parse_item'),
    )

    def parse_item(self, res):
        res.meta['item_body'] = res.body
        res.meta['item_url'] = res.url
        res.meta['item_data'] = res.pq('#content').text()

        yield Request(url=res.url, meta=res.meta,
                      callback=super(MusiciansFriendSpider, self).parse_item)

    def process_item_response(self, res):
        # re_match = re.search(r's7sdkJSONResponse\(({.+}),"[^"]+"\);', res.body)
        # res.meta['image_data'] = res.json(re_match.group(1))
        res = res.replace(body=res.meta['item_body'], url=res.meta['item_url'])
        res.pq = PyQuery(res.meta['item_body'])
        return res

    def parse_item_code(self, res):
        return res.meta['item_data']('.description li')[1].clone().remove('label').text()

    def parse_item_url(self, res):
        return res.urljoin(res.meta['item_data']['pageUrl'])

    def parse_item_name(self, res):
        return res.meta['item_data']('.product-title')

    def parse_item_description(self, res):
        return (fix_text(res.meta['item_data']('.std'))
                if res.meta['item_data']('.std') else '')

    def parse_item_brand(self, res):
        return res.meta['item_data']('.brand').clone().remove('label').text()

    def parse_item_color(self):
        return ''

    def parse_item_price(self, res):
        return format.price_format(res.pq('li.price-old').text() or
                                   res.pq('.prices').text())

    def parse_item_sale_price(self, res):
        selector = 'li.price-old'

        if not res.pq(selector):
            return 0

        price = self.parse_item_price(res)
        sale_price = res.pq(selector).text()
        return format.price_sale_format(price, sale_price)

    def parse_item_images(self, res):
        items = res.meta['item_data']('.thumbnails')
        return [items('a').attr('href') for i in items if 'cache' not in i.text().lower()]

    def parse_item_stock(self, res):
        return 'pre-order' not in res.meta['item_data']('.description li')[3]

    def parse_item_classifiers(self, res):
        categories = [item.text().lower().strip() for item in res.pq('.breadcrumb li').items()]
        return categories[-1]
