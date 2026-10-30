"""
ALeRCE Python Client
====================

A Python client for accessing ALeRCE astronomical data services.

Usage
-----
>>> from alerce.core import Alerce
>>> client = Alerce()
>>> objects = client.query_objects(survey="ztf", ra=10.0, dec=-20.0, radius=30)
"""

from .core import Alerce

__all__ = ["Alerce"]

# Managed by python-semantic-release (see pyproject.toml); do not edit by hand.
__version__ = "2.3.1"
