# -*- coding: utf-8 -*-
import json

import requests


class SendPipeline(object):

    settings = None

    def __init__(self, settings):
        self.settings = settings

        if not self.settings.get('SEND_ITEM_API_URL'):
            raise Exception('SEND_ITEM_API_URL must be set in order to use send pipeline!')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if self.settings.get('DEBUG'):
            return item

        res = requests.post(self.settings.get('SEND_ITEM_API_URL'), json=dict(item))
        status = res.status_code

        if status != 200:
            raise Exception('Bad response when sending data. Status code ({})'.format(status))

        data = json.loads(res.text)

        if not data['success']:
            raise Exception(data['reason'])

        return item
