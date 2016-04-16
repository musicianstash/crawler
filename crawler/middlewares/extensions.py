# -*- coding: utf-8 -*-
import json
from types import MethodType

from ftfy import fix_text

from pyquery import PyQuery


def pq_extension(self, query):
    if not hasattr(self, 'pq_instance'):
        self.pq_instance = PyQuery(self.body)

    return self.pq_instance(query)


def ftfy_extension(text):
    return fix_text(text)


def json_extension(self, json_text=False):
    if isinstance(json_text, bool):
        return json.loads(self.body)

    return json.loads(json_text)


class PyqueryDownloaderMiddleware(object):
    """A downloader middleware which adds pyquery instance to each response.
    """

    def process_response(self, request, response, spider):
        response.json = MethodType(json_extension, response)
        response.pq = MethodType(pq_extension, response)
        response.fix_text = ftfy_extension
        return response
