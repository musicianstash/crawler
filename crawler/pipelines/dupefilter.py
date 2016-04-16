# -*- coding: utf-8 -*-
from scrapy import signals, Field
from scrapy.xlib.pydispatch import dispatcher
from ..contrib.exceptions import DupeValidationException


class DupeFilterPipeline(object):
    unique_codes = []
    unique_filter_enabled = False

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def spider_opened(self, spider):
        if hasattr(spider, 'item') and hasattr(spider.item, 'unique_fields'):
            unique_fields = spider.item.unique_fields
            item_keys = spider.item().fields.keys()

            if unique_fields and not all(uf in item_keys for uf in unique_fields):
                raise Exception('Specified unique fields must match with item fields!')
            else:
                if hasattr(spider.item, 'unique_code_field') and spider.item.unique_code_field:
                    spider.item.fields['unique_code'] = Field()

                self.unique_filter_enabled = True

    def process_item(self, item, spider):
        """Adds primary key of item to a given spider. """
        if not self.unique_filter_enabled:
            return item

        unique_code = self._create_unique_code(item)

        if unique_code in self.unique_codes:
            spider.crawler.stats.inc_value('dupe_exceptions')
            message = 'Non unique item with code: {}'.format(unique_code)
            raise DupeValidationException(message)
        else:
            self.unique_codes.append(unique_code)

        if hasattr(item, 'unique_code_field') and item.unique_code_field:
            item['unique_code'] = unique_code

        return item

    def _create_unique_code(self, item):
        values = []

        for unique_field in item.unique_fields:
            values.append('' if item[unique_field] is None else str(item[unique_field]))

        code = ''.join(values)
        return code.replace(' ', '').lower()
