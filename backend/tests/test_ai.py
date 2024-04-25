import unittest
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))
from app.ai import is_predictive_query, create_ai_input

class TestAI(unittest.TestCase):


    # Testing if the query is predictive when the timestamp is in the future


    def test_is_predictive_query_future(self):
        query = {"timestamp": datetime.utcnow() + timedelta(days=1)}
        self.assertTrue(is_predictive_query(query))


    # Testing if the query is predictive when the timestamp is in the past


    def test_is_predictive_query_past(self):
        query = {"timestamp": datetime.utcnow() - timedelta(days=1)}
        self.assertFalse(is_predictive_query(query))


    # Testing if the query is not predictive when there is no timestamp

    def test_is_predictive_query_no_timestamp(self):
        query = {}
        self.assertFalse(is_predictive_query(query))

    def test_is_predictive_query_dict_timestamp(self):
        query = {"timestamp": {}}
        self.assertFalse(is_predictive_query(query))

    def test_create_ai_input(self):
        now = datetime.utcnow()
        query = {"timestamp": now}
        ai_input = create_ai_input(query)
        self.assertEqual(ai_input.queries, [query])
        self.assertTrue(ai_input.time_offset < timedelta(seconds=1))


if __name__ == '__main__':
    unittest.main()
