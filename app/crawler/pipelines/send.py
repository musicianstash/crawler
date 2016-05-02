# -*- coding: utf-8 -*-
import json

from txjsonrpc.jsonrpclib import VERSION_2
from txjsonrpc.web.jsonrpc import Proxy


class SendPipeline(object):

    settings = None

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_item(self, item, spider):
        if (self.settings.get('DEBUG') or not self.settings.get('SEND_ITEM_JSON_RPC_HOST') or
                not self.settings.get('SEND_ITEM_JSON_RPC_METHOD')):
            return item

        response = self.txjson_rpc_request(json.dumps(dict(item)))

        # res = requests.post(self.settings.get('SEND_ITEM_API_URL'), json=dict(item))
        # status = res.status_code
        #
        # if status != 200:
        #     raise Exception('Bad response when sending data. Status code ({})'.format(status))
        #
        # data = json.loads(res.text)
        #
        # if not data['success']:
            # raise Exception(data['reason'])

        return item

    def txjson_rpc_request(self, *params):
        """Twisted JSON call."""
        host = self.settings['SEND_ITEM_JSON_RPC_HOST']
        method = self.settings['SEND_ITEM_JSON_RPC_METHOD']
        services_endpoint = Proxy(host, version=VERSION_2)
        return services_endpoint.callRemote(method, *params)
