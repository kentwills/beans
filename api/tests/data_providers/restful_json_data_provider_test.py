# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import mock
import pytest
import urllib3
from yelp_beans.data_providers import restful_json_data_provider

MOCK_URL = "mock://example.com"


@pytest.fixture
def data_provider():
    return restful_json_data_provider.RestfulJSONDataProvider(
        MOCK_URL,
    )


@pytest.fixture
def authed_data_provider():
    return restful_json_data_provider.RestfulJSONDataProvider(
        MOCK_URL,
        username=mock.sentinel.username,
        password=mock.sentinel.password,
    )


def test_http_basic_authentication(authed_data_provider):
    headers = authed_data_provider._authentication()
    auth = '{}:{}'.format(mock.sentinel.username, mock.sentinel.password)
    expected_headers = urllib3.make_headers(basic_auth=auth)
    assert headers == expected_headers


def test_fetch(data_provider, employees):
    with mock.patch.object(urllib3.PoolManager, 'request', lambda http, url, headers, timeout: employees):
        result = data_provider._fetch(None)
        assert len(result) == 1
