# -*- coding: utf-8 -*-

from ftfy import fix_text

from pyquery import PyQuery
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from crawler.contrib.spiders.mixins.modular import ModularMixin
from crawler.items import MusicGearItem
from crawler.contrib import format

DENY_LINKS = ['extended-warranty', 'polarpro', 'drone-repair']


class InnovativeUASSpider(ModularMixin, CrawlSpider):
    name = 'innovativeuas.com'
    allowed_domains = ['innovativeuas.com']
    item = MusicGearItem

    spider_store = 'InnovativeUAS'
    spider_currency = 'USD'
    spider_countries = ['*']

    start_urls = ['https://www.innovativeuas.com/our-drones/']

    rules = (
        Rule(LinkExtractor(restrict_css='.product-category', deny=DENY_LINKS)),
        Rule(LinkExtractor(restrict_css='.woocommerce-LoopProduct-link'), callback='parse_item'),
    )

    def process_item_response(self, res):
        res.pq = PyQuery(res.body)
        return res

    def parse_item_code(self, res):
        return res.pq('input[name="add-to-cart"]').attr('value')

    def parse_item_url(self, res):
        return res.url

    def parse_item_name(self, res):
        return res.pq('.product-title').text()

    def parse_item_description(self, res):
        return fix_text(res.pq('[itemprop="description"]'))

    def parse_item_brand(self, res):
        return ''

    def parse_item_color(self, res):
        return ''

    def parse_item_price(self, res):
        return format.price_format(res.pq('.summary .woocommerce-Price-amount:eq(0)').text())

    def parse_item_sale_price(self, res):
        selector = '.summary .woocommerce-Price-amount:eq(1)'

        if not res.pq(selector):
            return 0

        price = self.parse_item_price(res)
        sale_price = res.pq(selector).text()
        return format.price_sale_format(price, sale_price)

    def parse_item_images(self, res):
        return [img.attr('href') for img in res.pq('.images a').items()]

    def parse_item_stock(self, res):
        return bool(res.pq('.single_add_to_cart_button'))
