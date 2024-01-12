import unittest
from tests.test_utils import *

class TestDBSchema(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        result = get_rest_call(self, 'http://localhost:5000/clubs')
        self.assertEqual(len(result), 4)

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        post_rest_call(self, 'http://localhost:5000/manage/init')
        post_rest_call(self, 'http://localhost:5000/manage/init')
        result = get_rest_call(self, 'http://localhost:5000/clubs')
        self.assertEqual(len(result), 4)
