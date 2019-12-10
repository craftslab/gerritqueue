#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import logging
import os
import sys

from .gerrit import Gerrit, GerritException
from .rqueue import Rqueue, RqueueException
from .version import VERSION


def _queue(changes, queue):
    found = False

    for item in changes:
        buf = queue.get(item)
        if buf is None or len(buf) == 0:
            queue.set(item)
        else:
            found = True

    return found, True


def _load(name):
    with open(name, 'r') as f:
        data = json.load(f)

    return data


def _logging(_level, name):
    if _level == logging.DEBUG:
        fmt = '%(filename)s: %(levelname)s: %(message)s'
    else:
        fmt = '%(levelname)s: %(message)s'

    if name is None:
        logging.basicConfig(format=fmt, level=_level)
    else:
        if not os.path.exists(name):
            logging.basicConfig(filename=name, format=fmt, level=_level)
        else:
            print('%s already exist' % name)
            return False

    return True


def main():
    global handler
    desc = 'Gerrit Queue'

    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f', '--config-file', dest='config_file',
                        help='config file, type: .json',
                        required=True)
    parser.add_argument('-q', '--gerrit-query', dest='gerrit_query',
                        help='gerrit query, format: QUERY1,QUERY2,...',
                        required=True)
    parser.add_argument('-v', '--version',
                        action='version',
                        version=VERSION)

    options = parser.parse_args()

    ret = _logging(logging.INFO, None)
    if ret is False:
        return -1

    if not os.path.exists(options.config_file) or not options.config_file.endswith('.json'):
        logging.error('Invalid config file %s' % options.config_file)
        return -2

    config = _load(options.config_file)

    if len(options.gerrit_query.strip()) == 0:
        logging.error('Invalid gerrit query %s' % options.gerrit_query)
        return -3

    gerrit_query = options.gerrit_query.strip().split(',')

    try:
        gerrit = Gerrit(config['gerrit'])
    except GerritException as e:
        logging.error(str(e))
        return -4

    changes = gerrit.query(gerrit_query)
    if changes is None or len(changes) == 0:
        logging.info('Change not found')
        return -5

    try:
        rqueue = Rqueue(config['redis'])
    except RqueueException as e:
        logging.error(str(e))
        return -6

    status = rqueue.connect()
    if status is False:
        logging.error('Failed to connect rqueue')
        return -7

    found, status = _queue(changes, rqueue)
    rqueue.disconnect()

    if status is False:
        logging.error('Failed to run _queue')
        return -8

    if found is True:
        logging.info('Change found in rqueue')
        ret = 1
    else:
        logging.info('Change added to rqueue')
        ret = 0

    logging.info('Done')

    return ret


if __name__ == '__main__':
    sys.exit(main())
