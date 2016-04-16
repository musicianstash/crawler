# -*- coding: utf-8 -*-
from scrapy import signals
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
                print("STOP SPIDER HERE")
            else:
                self.unique_filter_enabled = True

    def process_item(self, item, spider):
        """Adds primary key of item to a given spider. """
        return item
        # if not self.unique_filter_enabled:
        #     return item

        code = self._create_unique_code(item)

        if code in self.unique_codes:
            spider.crawler.stats.inc_value('dupe_exceptions')
            message = 'Non unique item with code: {}'.format(code)
            raise DupeValidationException(message)
        else:
            self.unique_codes.append(code)

        return item

    def _create_unique_code(self, item):
        values = []

        for unique_field in self.unique_fields:
            if unique_field not in item:
                pass

            values.append('' if item[unique_field] is None else item[unique_field])

        code = ''.join(values)
        item['unique_code'] = code.replace(' ', '')
        return item
