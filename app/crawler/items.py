# -*- coding: utf-8 -*-
import scrapy


class MusicGearItem(scrapy.Item):
    store = scrapy.Field()
    currency = scrapy.Field()
    countries = scrapy.Field()
    url = scrapy.Field()
    affiliate_url = scrapy.Field(default=None)
    code = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    brand = scrapy.Field()
    color = scrapy.Field(default='')
    price = scrapy.Field()
    sale_price = scrapy.Field()
    images = scrapy.Field()
    stock = scrapy.Field()
    classifiers = scrapy.Field()

    unique_code_field = True
    unique_fields = ['code', 'color']

    json_schema_validation = {
        'type': 'object',
        'properties': {
            'code': {'type': 'string'},
            'name': {
                'type': 'string',
                'minLength': 1,
                'maxLength': 120
            },
            'description': {'type': 'string'},
            'brand': {'type': 'string'},
            'price': {
                'type': 'number',
                'minimum': 2
            },
            'sale_price': {'type': 'number'},
            'images': {
                'type': 'array',
                'minItems': 1
            },
            'stock': {
                'anyOf': [
                    {'type': 'boolean'},
                    {'type': 'object', 'minProperties': 1}
                ]
            },
        },
        'required': ['store', 'currency', 'countries', 'url', 'affiliate_url', 'code', 'name',
                     'description', 'brand', 'color', 'price', 'sale_price', 'images', 'stock',
                     'classifiers']
    }
