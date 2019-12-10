#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import pprint
import redis


class RqueueException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Rqueue(object):
    def __init__(self, config):
        if config is None:
            raise RqueueException('Invalid rqueue config')

        self._db = config.get('db', 0)
        self._debug = config.get('debug', False)
        self._hash = config.get('hash', {'expire': {'days': 1}, 'key': 'current_revision', 'name': '_number'})
        self._host = config.get('host', 'localhost')
        self._pass = config.get('pass', None)
        self._port = config.get('port', 6379)

        self._redis = None

    def _expire(self):
        today = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
        _next = today + datetime.timedelta(days=self._hash['expire']['days'])
        now = datetime.datetime.now()

        return (_next - now).seconds

    def connect(self):
        try:
            self._redis = redis.Redis(host=self._host, port=self._port, db=self._db, password=self._pass)
        except redis.exceptions.ResponseError as _:
            return False

        return True

    def disconnect(self):
        def _disconnect(data):
            try:
                self._redis.client_kill(data)
            except redis.exceptions.ResponseError as _:
                pass

        for item in self._redis.client_list():
            _disconnect(item['addr'])

    def set(self, data):
        self._redis.set(data[self._hash['name']], data[self._hash['value']])
        self._redis.expire(data[self._hash['name']], self._expire())

    def delete(self, data):
        self._redis.delete(data[self._hash['name']])

    def get(self, data):
        return self._redis.get(data[self._hash['name']])


if __name__ == '__main__':
    def _load(name):
        with open(name, 'r') as f:
            data = json.load(f)

        return data

    config = _load(os.path.join(os.getcwd(), 'config.json'))
    change = _load(os.path.join(os.getcwd(), 'tests', 'change.json'))

    r = Rqueue(config['redis'])

    r.connect()

    r.set(change)
    buf = r.get(change)
    pprint.pprint(buf)

    change['current_revision'] = '0'
    r.set(change)
    buf = r.get(change)
    pprint.pprint(buf)

    r.delete(change)
    buf = r.get(change)
    pprint.pprint(buf)

    r.disconnect()
