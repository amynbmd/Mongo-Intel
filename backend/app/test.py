# tests for overall application

import nlp
import ai

from datetime import datetime
from datetime import timedelta




# NLP TEST
# verifies if we can translate natural language text into queries
def test_text_to_query():
    text = "Where is GMU?"
    expected_query = { "name": "GMU" }

    actual_query = nlp.text_to_query(text)
    assert actual_query == expected_query


# AI TEST
# verifies if we can make a prediction using AI
def test_predict_query():
    tomorrow = datetime.utcnow() + timedelta(days=1)
    query_input = { "name": "GMU", "timestamp": tomorrow }

    actual_query_result = ai.predict(query_input)
    assert actual_query_result != []