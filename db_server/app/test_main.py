from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from main import app

client = TestClient(app)

class TestMain(unittest.TestCase):
# Test that the '/positions' endpoint returns an empty list when there are no positions are available
    @patch('main.mongo_db.all_positions')
    async def test_list_positions(self, mock_all_positions):
        mock_all_positions.return_value = AsyncMock(return_value=[])
        response = client.get('/positions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"position_docs": []})

#check if the'/positions/{entity_id}' endpoint correctly retrieves a position when it exists
    @patch('main.mongo_db.find_position')
    async def test_get_position_found(self, mock_find_position):
        mock_find_position.return_value = AsyncMock(return_value={"entity_id": 1, "data": "some data"})
        response = client.get('/positions/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"entity_id": 1, "data": "some data"})

# ensure that the '/positions/{entity_id}' endpoint returns a 404 status code when the position does not exist
    @patch('main.mongo_db.find_position')
    async def test_get_position_not_found(self, mock_find_position):
        mock_find_position.return_value = AsyncMock(return_value=None)
        response = client.get('/positions/999')
        self.assertEqual(response.status_code, 404)

# test that the '/positions' endpoint returns a 200 status code and the created position when a new position is created
    @patch('main.mongo_db.insert_position')
    async def test_create_position(self, mock_insert_position):
        mock_insert_position.return_value = AsyncMock(return_value={"entity_id": 1, "data": "some data"})
        response = client.post('/positions', json={"data": "some data"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"entity_id": 1, "data": "some data"})

# verifies that the PUT /positions/{position_id} endpoint successfully modifies a position and returns the updated data.
    @patch('main.mongo_db.modify_position_by_id')
    async def test_modify_position(self, mock_modify_position_by_id):
        sample_position_id = "12345"
        sample_new_position = {"data": "updated data"}
        mock_modify_position_by_id.return_value = AsyncMock(return_value={"_id": sample_position_id, **sample_new_position})

        response = client.put(f'/positions/{sample_position_id}', json=sample_new_position)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"_id": sample_position_id, **sample_new_position})

# tests that the DELETE /positions/{position_id} endpoint successfully deletes a position and returns the appropriate status code (204 No Content).
    @patch('main.mongo_db.delete_position')
    async def test_delete_document(self, mock_delete_position):
        sample_position_id = "12345"
        mock_delete_position.return_value = AsyncMock(return_value=True)

        response = client.delete(f'/positions/{sample_position_id}')
        self.assertEqual(response.status_code, 204)
# Checks if the PUT /entity-positions/{entity_id} endpoint correctly updates a position based on the entity ID and returns the updated data.
    @patch('main.mongo_db.modify_position')
    async def test_modify_entity_position(self, mock_modify_position):
        sample_entity_id = 1
        sample_new_position = {"data": "updated entity data"}
        mock_modify_position.return_value = AsyncMock(return_value={"entity_id": sample_entity_id, **sample_new_position})

        response = client.put(f'/entity-positions/{sample_entity_id}', json=sample_new_position)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"entity_id": sample_entity_id, **sample_new_position})

# Test the POST /positions endpoint for invalid data
    @patch('main.mongo_db.insert_position')
    async def test_create_position_invalid_data(self, mock_insert_position):
        mock_insert_position.side_effect = AsyncMock(side_effect=ValueError("Invalid data"))
        response = client.post('/positions', json={"invalid": "data"})
        self.assertNotEqual(response.status_code, 200)
        print("Testing create position with invalid data...")
        print("Response status code:", response.status_code)

 # Test modifying a non-existent position
    @patch('main.mongo_db.modify_position_by_id')
    async def test_modify_nonexistent_position(self, mock_modify_position_by_id):
        sample_position_id = "nonexistent_id"
        sample_new_position = {"data": "new data"}
        mock_modify_position_by_id.return_value = AsyncMock(return_value=None)
        
        response = client.put(f'/positions/{sample_position_id}', json=sample_new_position)
        self.assertEqual(response.status_code, 404)
        print("Testing modify nonexistent position...")
        print("Response status code:", response.status_code)

# Test deleting a non-existent position
    @patch('main.mongo_db.delete_position')
    async def test_delete_nonexistent_document(self, mock_delete_position):
        sample_position_id = "nonexistent_id"
        mock_delete_position.return_value = AsyncMock(return_value=False)
        
        response = client.delete(f'/positions/{sample_position_id}')
        self.assertEqual(response.status_code, 404)
        print("Testing delete nonexistent document...")
        print("Response status code:", response.status_code)

# Test modifying entity position with invalid data
    @patch('main.mongo_db.modify_position')
    async def test_modify_entity_position_invalid_data(self, mock_modify_position):
        sample_entity_id = 999
        sample_new_position = {"invalid": "data"}
        mock_modify_position.return_value = AsyncMock(return_value=None)
        
        response = client.put(f'/entity-positions/{sample_entity_id}', json=sample_new_position)
        self.assertEqual(response.status_code, 404)
        print("Testing modify entity position with invalid data...")
        print("Response status code:", response.status_code)

if __name__ == '__main__':
    unittest.main()
