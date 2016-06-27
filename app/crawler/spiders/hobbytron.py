# -*- coding: utf-8 -*-

from pyquery import PyQuery
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from crawler.contrib.spiders.mixins.modular import ModularMixin
from crawler.items import MusicGearItem
from crawler.contrib import format


class HobbyTronSpider(ModularMixin, CrawlSpider):
    name = 'hobbytron.com'
    allowed_domains = ['hobbytron.com']
    item = MusicGearItem

    spider_store = 'HobbyTron'
    spider_currency = 'USD'
    spider_countries = ['US']

    download_delay = 0.5

    start_urls = ['http://www.hobbytron.com/Drones.html']

    rules = (
        Rule(LinkExtractor(restrict_css='.category')),
        Rule(LinkExtractor(restrict_css='.pagniation')),    # yes, its legit
        Rule(LinkExtractor(restrict_css='.search .image'), callback='parse_item'),
    )

    def process_item_response(self, res):
        res.pq = PyQuery(res.body)
        return res

    def parse_item_code(self, res):
        return res.pq('[itemprop="identifier"]').attr('content').split('sku:')[1]

    def parse_item_url(self, res):
        return res.url

    def parse_item_name(self, res):
        return res.pq('[itemprop="name"]').text()

    def parse_item_description(self, res):
        return res.pq('.description').text()

    def parse_item_brand(self, res):
        return (res.pq('.brand').clone().remove('label').text() or
                res.pq('[itemprop="name"]').text().split(' ')[0])

    def parse_item_color(self, res):
        return ''

    def parse_item_price(self, res):
        return format.price_format(res.pq('.reg').text())

    def parse_item_sale_price(self, res):
        selector = '.sale_amount'

        if not res.pq(selector):
            return 0

        price = self.parse_item_price(res)
        sale_price = format.price_format(res.pq(selector).text())
        return format.price_sale_format(price, sale_price)

    def parse_item_images(self, res):
        items = res.pq('.gallery_thumbs img')
        if not items:
            return [res.pq('.product_icons img').attr('src')]
        return [i.attr('src') for i in items.items()]

    def parse_item_stock(self, res):
        return bool(res.pq('.form_addtocart'))

    def parse_item_classifiers(self, res):
        categories = [item.text().lower().strip() for item in res.pq('.breadCrumb a').items()]
        return categories[-1]
