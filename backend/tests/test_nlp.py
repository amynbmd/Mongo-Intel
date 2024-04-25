import unittest
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

import nlp # importing the nlp module itself
from nlp import gen_query, convert_times, process_text, text_to_query
from unittest.mock import patch

class TestLocationQueries(unittest.TestCase):

    @patch('nlp.spacy_model.convert_question_to_query')
    def test_festival_location_query(self, mock_convert):
        mock_convert.return_value = '{"item": "truck-C22", "date": {"$eq": "2023-07-15T12:00:00"}}'

        question = "Where will the truck-C22 be located next Saturday at noon?"
        expected_query = '{"item": "truck-C22", "date": {"$eq": "2023-07-15T12:00:00"}}'
        
        generated_query = gen_query(question)
        mock_convert.assert_called_once_with(question)
        self.assertEqual(generated_query, expected_query)

    @patch('nlp.spacy_model.convert_question_to_query')
    def test_bobby_location_query(self, mock_convert):
        mock_convert.return_value = '{"name": "Bobby", "time": {"$eq": "10:00"}}'

        question = "where is Bobby at 10am?"
        expected_query = '{"name": "Bobby", "time": {"$eq": "10:00"}}'
        
        generated_query = gen_query(question)
        mock_convert.assert_called_once_with(question)
        self.assertEqual(generated_query, expected_query)

    # Add more test methods for other questions...

# Remember to include other test classes as well

if __name__ == '__main__':
    unittest.main()

  
class TestGenQuery(unittest.TestCase):

# testing the gen_query function in nlp.py
    @patch('nlp.nl2query_model.construct_query')
    @patch('nlp.spacy_model.convert_question_to_query')
    def test_gen_query_spacy_model(self, mock_spacy, mock_nl2query):
        mock_spacy.return_value = "spacy query"
        mock_nl2query.return_value = "nl2query query"

        question = "Where is the blue bird?"
        query = gen_query(question)
        mock_spacy.assert_called_once_with(question)
        self.assertEqual(query, "spacy query")

    @patch('nlp.nl2query_model.construct_query')
    @patch('nlp.spacy_model.convert_question_to_query')
    def test_gen_query_nl2query_model(self, mock_spacy, mock_nl2query):
        # Simulating changing the MODEL to 'nl2query'
        nlp.MODEL = "nl2query"
        mock_spacy.return_value = "spacy query"
        mock_nl2query.return_value = "nl2query query"

        question = "What's the weather tomorrow?"
        query = gen_query(question)
        mock_nl2query.assert_called_once_with(question)
        self.assertEqual(query, "nl2query query")

        # Reset MODEL to its default value
        nlp.MODEL = "spacy"

#Testing the convert_times function in nlp.py
class TestConvertTimes(unittest.TestCase):

    def test_convert_times_with_valid_timestamp(self):
        query = {"timestamp": {"$gte": "2023-01-01T00:00:00"}}
        updated_query = convert_times(query)
        self.assertIsInstance(updated_query["timestamp"]["$gte"], datetime)

    def test_convert_times_without_timestamp(self):
        query = {"name": "Eiffel Tower"}
        updated_query = convert_times(query)
        self.assertEqual(query, updated_query)

class TestProcessText(unittest.TestCase):

    @patch('nlp.gen_query')
    @patch('nlp.string_to_query')
    def test_process_text_valid_input(self, mock_string_to_query, mock_gen_query):
        mock_gen_query.return_value = "{name: 'Eiffel Tower'}"
        mock_string_to_query.return_value = {"name": "Eiffel Tower"}

        question = "What's the weather like in Paris?"
        result = process_text(question)
        self.assertIsNotNone(result)
        self.assertIn("name", result)

class TestTextToQuery(unittest.TestCase):

    @patch('nlp.process_text')
    def test_text_to_query(self, mock_process_text):
        mock_process_text.return_value = {"name": "Eiffel Tower"}

        question = "What's the height of the Eiffel Tower?"
        result = text_to_query(question)
        self.assertIsNotNone(result)
        self.assertIn("name", result)
        self.assertEqual(result["name"], "Eiffel Tower")

if __name__ == '__main__':
    unittest.main()
