# Handles query processing

import ai
import mongo_db
from mongo_db import PositionSnapshot, query_positions

import pprint
from datetime import datetime, date, time, timedelta
import json


# placeholders for resolving queries
# returns a list of position snapshot documents
async def resolve_query(query: dict, page: int) -> list[PositionSnapshot]:
    if query is None:
        print("QUERY_ERROR: Null query")
        return []

    # predictive query (AI query):
    if await ai.is_predictive_query(query):
        print("PAGE\n\n\n", page)
        ai_input = ai.create_ai_input(query)
        query_results = await ai.predict(ai_input)
        return query_results
    
    # non-predictive queries (simple query):
    else: query_results = await run_query(query, page)

    return query_results


async def run_query(query: dict, page: int) -> list[PositionSnapshot]:
    increment = page * 100  # skip by page amount in increments of 100

    matching_documents = await query_positions(query)
    matching_documents.skip(increment).limit(100)

    query_results = []
    async for document in matching_documents:
        query_results.append(document)

    return query_results


# method for testing queries
async def get_results(query: dict):
    print("Query: ")
    pprint.pprint(query)

    results = await resolve_query(query, 0)
    print("Results:")
    pprint.pprint(results)


# converts string to a dict if it is a valid JSON object
# returns None if string is not parseable
def string_to_query(string: str) -> dict | None:
    try:
        query = json.loads(string)
        return query
    except ValueError:
        return None


# Test queries:
name_query = {"name": "GMU"}

time_query = {
    "timestamp": {
        "$lt": datetime.combine(date(2023,10,15), time(10,00))
    }
}

location_query = { 
    'location': {
        '$geoWithin': {
            '$box': [
                [-90, 30],  # lower left corner of box
                [-60, 50],  # upper right corner of box
            ]
        }
    } 
}


if __name__ == "__main__":
    
    query = location_query  # <-- change this to modify the query, or make your own

    print()
    client = mongo_db.client
    loop = client.get_io_loop() # <-- for running async function `get_results()`
    loop.run_until_complete(get_results(query))
    print()
