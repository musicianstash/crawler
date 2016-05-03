# -*- coding: utf-8 -*-
import re

from ftfy import fix_text

from pyquery import PyQuery
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, Request

from crawler.contrib.spiders.mixins.modular import ModularMixin
from crawler.items import MusicGearItem
from crawler.contrib import format

DENY_LINKS = ['books', 'lifestyle', 'software', 'used']


class MusiciansFriendSpider(ModularMixin, CrawlSpider):
    name = 'musiciansfriend.com'
    allowed_domains = ['musiciansfriend.com']
    item = MusicGearItem

    spider_store = 'Musician Friend'
    spider_currency = 'USD'
    spider_countries = ['US']

    download_delay = 0.5

    start_urls = ['http://www.musiciansfriend.com/']

    rules = (
        Rule(LinkExtractor(restrict_css='#nav-content', deny=DENY_LINKS,
                           tags=['span'], attrs=['data-url'])),
        Rule(LinkExtractor(restrict_css='.searchPagination')),
        Rule(LinkExtractor(restrict_css='.productGrid .product', deny=DENY_LINKS),
             callback='parse_item'),
    )

    def parse_item(self, res):
        res.meta['item_body'] = res.body
        res.meta['item_url'] = res.url
        res.meta['item_data'] = res.json(res.pq('.adobeRecsProdData').text().strip())
        url = ('http://media.musiciansfriend.com/is/image/{}/?req=set,json,UTF-8&labelkey=label&'
               'id=17379552&handler=s7sdkJSONResponse')

        # one color items
        if not res.pq('#styleSelect .styleInfo'):
            scene7_id = res.pq('#initialScene7SetId').text()
            yield Request(url=url.format(scene7_id), meta=res.meta,
                          callback=super(MusiciansFriendSpider, self).parse_item)

        # multi color items
        for style_data in res.pq('#styleSelect .styleInfo').items():
            meta = res.meta.copy()
            meta['color_data'] = res.json(style_data.text().strip())
            image_url = url.format(meta['color_data']['scene7SetID'])
            yield Request(url=image_url, meta=meta,
                          callback=super(MusiciansFriendSpider, self).parse_item)

    def process_item_response(self, res):
        re_match = re.search(r's7sdkJSONResponse\(({.+}),"[^"]+"\);', res.body)
        res.meta['image_data'] = res.json(re_match.group(1))
        res = res.replace(body=res.meta['item_body'], url=res.meta['item_url'])
        res.pq = PyQuery(res.meta['item_body'])
        return res

    def parse_item_code(self, res):
        return res.meta['item_data']['id']

    def parse_item_url(self, res):
        return res.urljoin(res.meta['item_data']['pageUrl'])

    def parse_item_name(self, res):
        return res.meta['item_data']['name']

    def parse_item_description(self, res):
        return (fix_text(res.meta['item_data']['message'])
                if res.meta['item_data']['message'] else '')

    def parse_item_brand(self, res):
        return res.meta['item_data']['brand']

    def parse_item_color(self, res):
        return res.meta['color_data']['name'] if res.meta.get('color_data') else ''

    def parse_item_price(self, res):
        if res.meta.get('color_data'):
            price = res.meta['color_data'].get('msrp') or res.meta['color_data'].get('price')
            return format.price_format(price)
        return format.price_format(res.pq('#itemizedPrice .listPrice dd').text() or
                                   res.pq('[itemprop="price"]').text())

    def parse_item_sale_price(self, res):
        if res.meta.get('color_data'):
            return res.meta['color_data']['salePrice']

        if not res.pq('.onSaleToday'):
            return 0

        price = self.parse_item_price(res)
        sale_price = res.pq('.topAlignedPrice').clone().remove('sup').text()
        return format.price_sale_format(price, sale_price)

    def parse_item_images(self, res):
        items = res.meta['image_data']['set']['item']
        items = [items] if type(items) is not list else items
        image_url = 'http://media.musiciansfriend.com/is/image/{}?wid=2000&hei=2000'
        return [image_url.format(i['i']['n']) for i in items]

    def parse_item_stock(self, res):
        if res.meta.get('color_data'):
            return 'instock' in res.meta['color_data']['status']

        return 'in_stock' in res.pq('.availability').text()

    def parse_item_classifiers(self, res):
        categories = [item.text().lower().strip() for item in res.pq('.breadcrumbs a').items()]
        return categories[-1]
