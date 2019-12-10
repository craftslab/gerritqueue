# gerritqueue

[![PyPI](https://img.shields.io/pypi/v/gerritqueue.svg?color=brightgreen)](https://pypi.org/project/gerritqueue/)
[![License](https://img.shields.io/github/license/craftslab/gerritqueue.svg?color=brightgreen)](https://github.com/craftslab/gerritqueue/blob/master/LICENSE)

*Gerrit Queue* is a Gerrit event queue using Redis.



## Requirements

- Python (3.7+)
- pip
- redis



## Installation

```bash
apt update
apt install python3-dev python3-pip python3-setuptools
pip install gerritqueue
```



## Updating

```bash
pip install gerritqueue --upgrade
```



## Running

```bash
gerritqueue \
  --config-file config.json \
  --gerrit-query "change:1"
```



## Settings

*Gerrit Queue* parameters can be set in the file of [config.json](https://github.com/craftslab/gerritqueue/blob/master/config.json).

An example of configuration in config.json
```
{
  "gerrit": {
    "debug": false,
    "host": "localhost",
    "pass": "pass",
    "port": 80,
    "query": {
      "option": ["CURRENT_REVISION"]
    },
    "user": "user"
  },
  "redis": {
    "db": 0,
    "debug": false,
    "hash": {
      "expire": {
        "days": 1
      },
      "name": "_number",
      "value": "current_revision"
    },
    "host": "localhost",
    "pass": "pass",
    "port": 6379
  }
}
```



## Redis

```
Name           Value
CHANGE_NUMBER  CURRENT_REVISION
```



## License Apache

Project License can be found [here](https://github.com/craftslab/gerritqueue/blob/master/LICENSE).
