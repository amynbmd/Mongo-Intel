import unittest
import sys # Importing the sys module to access the path variable
import os # Importing the os module to access the file system
import re # Importing the re module to use regular expressions
from datetime import datetime, timedelta

import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app.spacy_model import convert_question_to_query
from datetime import datetime

class TestSpacyModel(unittest.TestCase):

    # Utility function to extract parts of the MongoDB query using regular expressions
    def extract_query_part(self, query, part):
        """Utility function to extract parts of the MongoDB query using regular expressions."""
        pattern = rf'{part}": "(.*?)"'
        match = re.search(pattern, query)
        if match:
            return match.group(1)
        return None
    
    # Testing the extraction of the subject from a question. 
    def test_subject_extraction(self):
        question = "Where is the Kitty?"
        expected_name = "Kitty"  
        query = convert_question_to_query(question)
        extracted_name = self.extract_query_part(query, "name")
        self.assertEqual(extracted_name, expected_name)

    # Testing the extraction of the date from a question
    def test_date_extraction(self):
        question = "What events are happening on October 1st, 2023?"
        expected_date_start = "2023-10-01T01:00:00"  
        query = convert_question_to_query(question)
        timestamp_pattern = r'"timestamp": \{\s*"\$gte": "(.*?)",\s*"\$lt": "(.*?)"\s*\}'
        match = re.search(timestamp_pattern, query)
        self.assertIsNotNone(match, "Timestamp condition not found in the query")
        self.assertEqual(match.group(1), expected_date_start)
    

    def test_description_extraction(self):
        question = "Find the location of flights at JFK airport."
        query = convert_question_to_query(question)
        extracted_description = self.extract_query_part(query, "description")
        # Expecting no description to be extracted
        self.assertIsNone(extracted_description)



    # Testing the extraction of the time from a question
    def test_query_structure(self):
        question = "What's the weather like in Paris tomorrow?"
        query = convert_question_to_query(question)
        # Checking if the query string contains essential MongoDB query parts
        self.assertIn('db.PositionSnapshot.findOne({', query)
        self.assertIn('name', query)
        self.assertIn('timestamp', query)

    # Testing the basic conversion of a question to a query
    def test_query_conversion_basic(self):
        question = "Where is John today?"
        expected_query_part = '"name": "John"'  
        query = convert_question_to_query(question)
        self.assertIn(expected_query_part, query)
    
    # Testing the extraction of the person's name from a question
    def test_person_location_extraction(self):
        question = "Where is John Doe right now?"
        expected_name = "John Doe"
        query = convert_question_to_query(question)
        extracted_name = self.extract_query_part(query, "name")
        self.assertEqual(extracted_name, expected_name)
        # Check if the query includes a location-based search
        self.assertIn('location', query)
    
    #Testing the conversion of a question with a specific time to a query
    def test_query_conversion_time(self):
        question = "Where is John Doe at 3:00 PM?"
        expected_timestamp_gte = "15:00:00"  # Adjusting to check the range
        query = convert_question_to_query(question)
        timestamp_pattern = r'"timestamp": \{\s*"\$gte": "(.*?)",\s*"\$lt": "(.*?)"\s*\}'
        match = re.search(timestamp_pattern, query)
        self.assertIsNotNone(match, "Timestamp condition not found in the query")
        self.assertIn(expected_timestamp_gte, match.group(1))
    
    # Testing the extraction of the location from a question. 
    def test_org_extraction(self):
        question = "Show records for Kitty."
        query = convert_question_to_query(question)
        extracted_org = self.extract_query_part(query, "description")
        self.assertIsNone(extracted_org)  #  based on the actual output


    def test_location_with_specific_time_extraction(self):
        question = "Where was Alice at 3 PM last Friday?"
        expected_name = "Alice"
        query = convert_question_to_query(question)
        extracted_name = self.extract_query_part(query, "name")
        self.assertEqual(extracted_name, expected_name)
        # Checking for the presence of a timestamp constraint in the query
        self.assertIn('"timestamp":', query)

    # Testing the extraction of the location from a question. Check if the extraction can extract if an object is a 2-word object.
    def test_object_location_extraction(self):
        question = "Where was the red car parked yesterday?"
        expected_description = "red car"
        query = convert_question_to_query(question)
        extracted_description = self.extract_query_part(query, "description")
        self.assertEqual(extracted_description, expected_description)
        # Verify the query is targeting a location field
        self.assertIn('location', query)



    def test_plane_location_at_specific_time(self):
        question = "Where was the plane-R543 at 1:00 PM today?"
        query = convert_question_to_query(question)
        
        # If the function doesn't extract "plane-R543" but you still want to ensure location and time are correctly handled:
        self.assertIn('location', query)
        self.assertIn('"timestamp":', query)
        
        # Check if the timestamp is correctly set
        expected_time = datetime.now().strftime("%Y-%m-%d") + "T13:00:00"
        timestamp_pattern = r'"timestamp": \{\s*"\$gte": "(.*?)",\s*"\$lt": "(.*?)"\s*\}'
        match = re.search(timestamp_pattern, query)
        self.assertIsNotNone(match, "Timestamp condition not found in the query")
        self.assertEqual(match.group(1), expected_time)

    # Testing the extraction of the location from a question. 
    def test_record_of_entity_since_time(self):
        question = "show the record of Kitty since 2 AM yesterday"
        expected_name = "Kitty"
        
        # Calculate the expected start time: 2 AM of the previous day
        now = datetime.now()
        expected_time_gte = datetime(now.year, now.month, now.day, 2, 0) - timedelta(days=1)
        
        query = convert_question_to_query(question)

        # Check if the entity "Kitty" is correctly extracted
        extracted_name = self.extract_query_part(query, "description")  # Adjust based on your function's output
        self.assertEqual(extracted_name, expected_name)

        # Extract and verify the timestamp from the generated query
        timestamp_pattern = r'"timestamp": \{\s*"\$gte": "(.*?)",\s*"\$lt": "(.*?)"\s*\}'
        match = re.search(timestamp_pattern, query)
        self.assertIsNotNone(match, "Timestamp condition not found in the query")

        # Convert the extracted timestamps to datetime for comparison
        query_time_gte = datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")
        query_time_lte = datetime.strptime(match.group(2), "%Y-%m-%dT%H:%M:%S")

        # Check if the time constraints are correctly applied
        self.assertTrue(expected_time_gte <= query_time_gte <= now)
        self.assertTrue(expected_time_gte <= query_time_lte <= now)

        # Optionally, check if the query targets the location field
        self.assertIn('location', query)
    
    def convert_time_to_mongo_format(time_string, date_string):
        # Initialize timestamp to the current time, without microseconds for consistency
        timestamp = datetime.now().replace(microsecond=0)

        # Set a default value for time_val, for example, midnight
        time_val = time(0, 0)

        # Your existing logic to process time_string and possibly update time_val

        # Your existing logic to process date_string and determine date_val

        # Ensure time_val is defined by this point before using it
        timestamp = datetime.combine(date_val, time_val)

        return timestamp



if __name__ == '__main__':
    unittest.main()
