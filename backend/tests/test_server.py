import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from server import app

client = TestClient(app)

#each test case tests a different function in server.py
class TestServer(unittest.TestCase):

    @patch('server.resolve_query')
    async def test_direct_query_valid(self, mock_resolve_query):
        mock_resolve_query.return_value = AsyncMock(return_value=[{"name": "GMU"}])

        response = client.get('/direct?query={"name":"GMU"}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"name": "GMU"}])

    @patch('server.resolve_query')
    async def test_direct_query_invalid(self, mock_resolve_query):
        mock_resolve_query.side_effect = AsyncMock(side_effect=ValueError("Invalid query"))

        response = client.get('/direct?query=invalid_query')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Cannot parse query", response.json().get('detail'))

    @patch('server.nlp.text_to_query')
    @patch('server.resolve_query')
    async def test_natural_language_query(self, mock_resolve_query, mock_text_to_query):
        mock_text_to_query.return_value = {"name": "GMU"}
        mock_resolve_query.return_value = AsyncMock(return_value=[{"name": "GMU"}])

        response = client.get('/nlp?text=Where is GMU')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"name": "GMU"}])

    # You can add more tests for other endpoints like /time, /geocode, etc.

if __name__ == '__main__':
    unittest.main()
