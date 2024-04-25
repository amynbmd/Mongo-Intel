# handles NLP functions for Mongo-Intel project
from query import string_to_query
import nl2query_model
import spacy_model

import datetime

MODEL = "spacy"

#This function takes in a natural language question and returns a MongoDB query
def gen_query(natural_language: str) -> str:
    if MODEL == "nl2query":
        return nl2query_model.construct_query(natural_language)
    elif MODEL == "spacy":
        return spacy_model.convert_question_to_query(natural_language)
    else:
        print("MODEL_ERROR: Unknown Model")

#This function takes in a query and converts the time strings to datetime objects
def convert_times(query: dict):
    if query.get("timestamp") == None:
        return query

    print(query)

    ts: dict = query.get("timestamp")
    for op, time in ts.items():
        ts[op] = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")

    return query


def process_text(natural_language: str) -> dict | None:

    generated_query = gen_query(natural_language)
    print(f"Initial query: {generated_query}")

    open = generated_query.find("{") 
    close = generated_query.find("}")+1 

    if open == -1 or close == -1: 
        print(f"NLP_ERROR: Irregular query")
        return None

    query_portion = generated_query[open:close] if MODEL == "nl2query" else generated_query[open:close]+"}" 
    query = string_to_query(query_portion)
    
    if query == {}:
        print("NLP_ERROR: Query too general")
        return None

    query = convert_times(query)
    print(f"Generalized query: {query}")

    return query


def text_to_query(text: str) -> dict:
    query = process_text(text)
    return query

# # #testing the output of the dictionary
# if __name__ == "__main__":
#     text = "Where is Bird-135292239 on 6/25/2017?"
#     print(text_to_query(text))
