# -*- coding: utf-8 -*-


class FormatPipeline(object):
    def process_item(self, item, spider):
        item = self._format_item_code(item)
        return item

    def _format_item_code(self, item):
        code = '{}{}'.format(item['code'].strip(), item['color'].strip()).upper()
        item['code'] = code.replace(' ', '')
        return item
