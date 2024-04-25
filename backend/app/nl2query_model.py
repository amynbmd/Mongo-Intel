from nl2query import MongoQuery

# model that allows us to generate queries
# inputs: document keys/attributes, and collection name 
queryfier = MongoQuery(
    collection_keys=[
        "_id", 
        "index",
        "entity_id",
        "name",
        "description",
        "location",
        "elevation",
        "timestamp",
        "bearing",
        "speed",
    ], 
    collection_name="positionSnapshot"
)

def construct_query(natural_language: str) -> str: 
    return queryfier.generate_query(f'''{natural_language}''')