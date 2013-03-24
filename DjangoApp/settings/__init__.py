# -*- mode: python; coding: utf-8; -*-
""" Settings for DjangoApp """

from .base import *
try:
    from .local import *
except ImportError, exc:
    exc.args = tuple(
        ['%s (did you rename settings/local-dist.py?)' % exc.args[0]])
    raise exc
