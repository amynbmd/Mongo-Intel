import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

import query
from mongo_db import PositionSnapshot

#each test case tests a different function in query.py
class TestQuery(unittest.TestCase):

    @patch('query.ai.is_predictive_query')
    @patch('query.ai.create_ai_input')
    @patch('query.ai.predict')
    async def test_resolve_query_predictive(self, mock_predict, mock_create_ai_input, mock_is_predictive_query):
        mock_is_predictive_query.return_value = True
        mock_create_ai_input.return_value = {}
        mock_predict.return_value = [PositionSnapshot()]

        result = await query.resolve_query({}, 0)
        self.assertEqual(len(result), 1)
        mock_predict.assert_called_once()

    @patch('query.query_positions')
    async def test_run_query(self, mock_query_positions):
        mock_query_positions.return_value = MagicMock()
        mock_query_positions.return_value.skip.return_value.limit.return_value.to_list.return_value = [PositionSnapshot()]

        result = await query.run_query({}, 0)
        self.assertEqual(len(result), 1)

    def test_string_to_query_valid(self):
        test_string = '{"name": "test"}'
        result = query.string_to_query(test_string)
        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'test')

    def test_string_to_query_invalid(self):
        test_string = 'not a json string'
        result = query.string_to_query(test_string)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
