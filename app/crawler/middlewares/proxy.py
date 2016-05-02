# -*- coding: utf-8 -*-
import re
import random
import base64


class ProxyDownloaderMiddleware(object):
    """A downloader middleware which uses rotating proxies.
    """
    proxy_address = None
    proxy_user_pass = None

    def __init__(self, settings):
        proxy_url = random.choice(settings.get('PROXIES', []))

        if proxy_url:
            proxy_parts = re.match('(\w+://)(\w+:\w+@)?(.+)', proxy_url)
            self.proxy_address = proxy_parts.group(1) + proxy_parts.group(3)

            if proxy_parts.group(2):
                self.proxy_user_pass = proxy_parts.group(2)[:-1]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta and not self.proxy_user_pass and self.proxy_address:
            return

        request.meta['proxy'] = self.proxy_address
        if self.proxy_user_pass:
            basic_auth = 'Basic ' + base64.b64encode(self.proxy_user_pass)
            request.headers['Proxy-Authorization'] = basic_auth
