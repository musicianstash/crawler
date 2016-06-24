# -*- coding: utf-8 -*-
class ModularMixin(object):

    def parse_item(self, response):
        if hasattr(self, 'process_item_response'):
            response = self.process_item_response(response)

        if hasattr(self, 'parse_items'):
            for context in self.parse_items(response):
                response.meta['gen'] = context
                yield self.parse_single_item(response)
        else:
            yield self.parse_single_item(response)

    def parse_single_item(self, response):
        item = self.item()

        if hasattr(self, 'item_config'):
            for key, value in self.item_config.items():
                item[key] = value

        for item_field in item.fields.keys():
            parse_item_field_method = 'parse_item_{}'.format(item_field)
            spider_field_method = 'spider_{}'.format(item_field)

            if hasattr(self, parse_item_field_method):
                item[item_field] = getattr(self, parse_item_field_method)(response)
            elif hasattr(self, spider_field_method):
                item[item_field] = getattr(self, spider_field_method)
            elif 'default' in item.fields[item_field]:
                item[item_field] = item.fields[item_field]['default']

        return item

    def process_item_resposne(self, response):
        return response
