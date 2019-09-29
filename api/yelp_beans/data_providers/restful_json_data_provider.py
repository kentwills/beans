# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json

import urllib3
from yelp_beans.data_providers.data_provider import DataProvider


class RestfulJSONDataProvider(DataProvider):

    def __init__(self, url, username=None, password=None, timeout=60.0):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout

    def _authentication(self):
        if self.username and self.password:
            auth = '{}:{}'.format(self.username, self.password)
            headers = urllib3.make_headers(basic_auth=auth)
            return headers

    def _fetch(self, data):
        http = urllib3.PoolManager()
        headers = self._authentication()
        result = http.request('GET', self.url, headers=headers, timeout=self.timeout)
        return json.loads(result)
