# -*- coding: utf-8 -*-
from ftfy import fix_text

import simplejson
from pyquery import PyQuery
from scrapy.spiders import CrawlSpider, Rule
from scrapy.link import Link
from scrapy.http import HtmlResponse

from crawler.contrib.spiders.mixins.modular import ModularMixin
from crawler.items import MusicGearItem


class CustomProductLinkExtractor():

    def extract_links(self, response):
        data = simplejson.loads(response.body)
        return [Link(url='https://www.dronesetc.com/products/{}.json'.format(product['handle']))
                for product in data['products']]


class DronesEtcSpider(ModularMixin, CrawlSpider):
    name = 'dronesetc.com'
    allowed_domains = ['dronesetc.com']
    item = MusicGearItem

    spider_store = 'DronesEtc'
    spider_currency = 'EUR'
    spider_countries = ['*']

    download_delay = 0.5

    start_urls = ['https://www.dronesetc.com/products.json']

    rules = (
        Rule(CustomProductLinkExtractor(), callback='parse_item'),
    )

    def _requests_to_follow(self, response):
        response = HtmlResponse(
            url=response.url, status=response.status, headers=response.headers,
            body=response.body, flags=response.flags, request=response.request)
        return super(DronesEtcSpider, self)._requests_to_follow(response)

    def process_item_response(self, res):
        res.meta['data'] = simplejson.loads(res.body)['product']
        return res

    def parse_item_code(self, res):
        return str(res.meta['data']['id'])

    def parse_item_url(self, res):
        return 'https://www.dronesetc.com/products/{}'.format(res.meta['data']['handle'])

    def parse_item_name(self, res):
        return res.meta['data']['title']

    def parse_item_description(self, res):
        return fix_text(PyQuery(res.meta['data']['body_html']).text())

    def parse_item_brand(self, res):
        return res.meta['data']['vendor']

    def parse_item_color(self, res):
        return ''

    def parse_item_price(self, res):
        variant = res.meta['data']['variants'][0]
        return float(variant['compare_at_price'] or variant['price'])

    def parse_item_sale_price(self, res):
        variant = res.meta['data']['variants'][0]
        return float(variant['price'])

    def parse_item_images(self, res):
        return [img['src'] for img in res.meta['data']['images']]

    def parse_item_stock(self, res):
        variant = res.meta['data']['variants'][0]
        return variant['inventory_quantity'] > 0

    def parse_item_classifiers(self, res):
        categories = [tag.lower().strip() for tag in res.meta['data']['tags'].split(',')]
        return categories[-1]
