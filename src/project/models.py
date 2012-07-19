from django.core.cache import cache
from django.test import TestCase


class ClearCacheTestCase(TestCase):
    """
    Clear cache manually because django.test.TestCase only truncates db tables.
    """

    def setUp(self):
        cache.clear()
        super(ClearCacheTestCase, self).setUp()
