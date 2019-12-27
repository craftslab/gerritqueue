#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import pprint
import requests


class GerritException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Gerrit(object):
    def __init__(self, config):
        if config is None:
            raise GerritException('Invalid gerrit config')

        self._debug = config.get('debug', False)
        self._pass = config.get('pass', None)
        self._query = config.get('query', {'option': ['CURRENT_REVISION']})
        self._url = 'http://' + config.get('host', 'localhost') + ':' + str(config.get('port', 80)) + '/a'
        self._user = config.get('user', None)

    def get(self, _id):
        response = requests.get(url=self._url+'/changes/'+str(_id)+'/detail', auth=(self._user, self._pass))
        if response.status_code != requests.codes.ok:
            return None

        return json.loads(response.text.replace(")]}'", ''))

    def query(self, search):
        payload = {
            'o': self._query['option'],
            'q': search
        }

        response = requests.get(url=self._url+'/changes/', auth=(self._user, self._pass), params=payload)
        if response.status_code != requests.codes.ok:
            return None

        return json.loads(response.text.replace(")]}'", ''))


if __name__ == '__main__':
    def _load(name):
        with open(name, 'r') as f:
            data = json.load(f)

        return data

    config = _load(os.path.join(os.getcwd(), 'config.json'))

    g = Gerrit(config['gerrit'])

    buf = g.get(1)
    pprint.pprint(buf)

    buf = g.query('change:1')
    pprint.pprint(buf)
