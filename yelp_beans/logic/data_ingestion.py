# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
from pydoc import locate

from yelp_beans.logic.config import get_config

DEFAULT_AVATAR = (
    'http://s3-media4.fl.yelpcdn.com'
    '/assets/srv0/yelp_large_assets/3f74899c069c/'
    'assets/img/illustrations/mascots/darwin@2x.png'
)


class DataIngestion(object):

    def __init__(self, *args, **kwargs):
        self.data_providers = []
        data_providers = get_config()['data_providers']
        for provider in data_providers:
            cls = locate(provider['class'])
            kwargs_keys = set(provider.keys()) - set(['class'])
            kwargs = {key: provider[key] for key in kwargs_keys}
            self.data_providers.append(cls(**kwargs))

    def ingest(self):
        data = {}
        for provider in self.data_providers:
            data[provider.__class__.__name__] = provider.ingest(data)
        return self.munge(data)

    def munge(self, external_data):
        employee_data = external_data['RestfulJSONDataProvider']
        s3_data = self.munge_s3(external_data['S3DataProvider'])
        for data in employee_data:
            data['email'] = data['metadata']['work_email']
            # TODO fix once we find a solution for photos
            data['photo_url'] = s3_data[data['email']].get('photo_url', DEFAULT_AVATAR)
            data['metadata'].update({
                'supervisory_organization': data['metadata']['supervisory_organization'],
                'department': data['metadata']['supervisory_organization'],
                'company_profile_url': data['metadata'].get('yelp_url'),
                'username': data['email'].split('@')[0]
            })
        return employee_data

    def munge_s3(self, old_data):
        new_data = defaultdict(dict)
        for data in old_data:
            photo_url = data['metadata']['photos'].get('ls', DEFAULT_AVATAR)
            if photo_url:
                photo_url.replace('http', 'https')
            email = data['metadata']['username'] + '@yelp.com'
            new_data[email]['photo_url'] = photo_url
        return new_data
