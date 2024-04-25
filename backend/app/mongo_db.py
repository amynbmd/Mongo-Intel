# handles MongoDB functions, aka defining the schema and evaluating queries
from motor import motor_asyncio

from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


# represents '_id' field in MongoDB. see explanation `db_server/mongo_db.py`
PyObjectId = Annotated[str, BeforeValidator(str)]

# GeoJSON object to specify geospatial location in MongoDB
class GeoJSONLocation(BaseModel):
    type: str = "Point"
    coordinates: tuple[float, float]    # format must be [longitude, latitude]

# data model formatted to be inserted into database
# IMPORTANT: keep this the same as the 'PositionSnapshotDocument' schema in `db_server/mongo_db.py`
class PositionSnapshot(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    entity_id: int
    name: str
    description: str | None = None
    location: GeoJSONLocation
    elevation: float | None = None
    timestamp: datetime
    heading: float
    speed: float


# MongoDB database connection and collection
client = motor_asyncio.AsyncIOMotorClient("192.168.1.46", 27017)
db = client.get_database("mongo-intel")
positions_collection = db.get_collection("positions")


# function below returns a 'cursor' which needs to be iterated through
# the query can be empty {} if we want to return all documents
async def query_positions(query: dict):
    positions = positions_collection.find(query)
    return positions


async def find_most_recent(query: dict):
    name = query.get("name")
    if name == None:
        return None
    
    most_recent_position = await positions_collection.find_one(
        {"name": name}, 
        sort=[("timestamp", -1)]
    )

    print(most_recent_position, type(most_recent_position))
    return most_recent_position

