# [ALeRCE](http://alerce.science) Client
[![Documentation Status](https://readthedocs.org/projects/alerce/badge/?version=latest)](https://alerce.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.com/alercebroker/alerce_client.svg?branch=master)](https://travis-ci.com/alercebroker/alerce_client) [![PyPI version](https://badge.fury.io/py/alerce.svg)](https://badge.fury.io/py/alerce)

The ALeRCE client gives a easy python interface with ALeRCE services.

## Documentation

The documentation of the client can be found [here](https://alerce.readthedocs.io/)

## API interface

The client can be used to query different ALeRCE APIs.

```python
  from alerce.api import AlerceAPI

  api = AlerceAPI()
  api.query(params)
```

The API class documentation can be found [here](https://alerce.readthedocs.io/en/latest/api.html)


## Installation

The installation of the ALeRCE client can be done with pip.
```bash
  pip install alerce
```

If you want to install the client from source just run
```bash
  python setup.py install
```
