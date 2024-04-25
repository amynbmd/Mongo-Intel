from motor import motor_asyncio

from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from bson import ObjectId



# handles MongoDB '_id' field (converts BSON ObjectId to string)
# view explanation in the 'The _id attribute and ObjectIds' section 
# of "https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/"
PyObjectId = Annotated[str, BeforeValidator(str)]


# GeoJSON object to specify geospatial location in MongoDB
class GeoJSONLocation(BaseModel):
    type: str = "Point"
    coordinates: tuple[float, float]    # format must be [longitude, latitude]


# data model we will take as input from user
class PositionSnapshot(BaseModel):
    name: str
    entity_id: int                      # unique to specific entity, even if its location or timestamp change
    description: str | None
    coordinates: tuple[float, float]    # format must be [longitude, latitude]
    elevation: float | None = None      # measured in meters, default is None
    timestamp: datetime
    heading: float                      # Heading is typically based on cardinal directions, so 0° (or 360°) indicates a direction toward true north, 90° true east, 180° true south, and 270° true west.
    speed: float                        # Speed over ground in m/s


# data model formatted to be inserted into database
class PositionSnapshotDocument(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)     # _id field for MongoDB
    entity_id: int                      # entity id field specific to entity (see description in PositionSnapshot)
    name: str
    description: str | None = None
    location: GeoJSONLocation
    elevation: float | None = None      # (see description in PositionSnapshot)
    timestamp: datetime
    heading: float
    speed: float


# data model used to UPDATE position documents
# since updates can involve partial changes, every attribute is optional
class UpdatePositionSnapshot(BaseModel):
    name: Optional[str] = None
    entity_id: Optional[int] = None
    description: Optional[str] = None
    coordinates: Optional[tuple[float, float]] = None
    elevation: Optional[float] = None
    timestamp: Optional[datetime] = None
    heading: float
    speed: float


# encapsulates PositionSnapshots
class PositionSnapshotCollection(BaseModel):
    position_docs: list[PositionSnapshotDocument]


# converts user input to a dict, so it can be inserted into the database
def position_to_document(position: PositionSnapshot):
    
    # convert coordinates into GeoJSON location, and prepare document format
    document = PositionSnapshotDocument(
        name=position.name,
        entity_id=position.entity_id,
        description=position.description,
        location=GeoJSONLocation(coordinates=position.coordinates),
        elevation=position.elevation,
        timestamp=position.timestamp,
        heading=position.heading,
        speed=position.speed
    )

    # convert position snapshot document object into dictionary
    document = document.model_dump(by_alias=True, exclude="_id")

    return document



# MongoDB database connection 
client = motor_asyncio.AsyncIOMotorClient("192.168.1.46", 27017)
db = client.get_database("mongo-intel")
positions_collection = db.get_collection("positions")



# database CRUD operations:

async def insert_position(position: PositionSnapshot):
    position_document = position_to_document(position)
    
    new_position = await positions_collection.insert_one(position_document) 
    created_position = await positions_collection.find_one({"_id": new_position.inserted_id})
    
    return created_position


async def all_positions(page: int):
    increment = page * 100  # skip by page amount in increments of 100

    cursor = positions_collection.find()
    cursor.skip(increment).limit(100)

    positions_docs = []
    async for document in cursor:
        positions_docs.append(document)

    return positions_docs


async def find_position(position_id: int):
    if (position := await positions_collection.find_one({"entity_id": position_id})) is not None:
        return position
    else:
        return None


async def modify_position(entity_id: int, position: UpdatePositionSnapshot):
    # encapsulates coords in GeoJSON object if it is present
    if position.coordinates is not None:
        coords = position.coordinates
        position.coordinates = GeoJSONLocation(coordinates=coords)

    # create document (dict) from given position, only store values that are not null
    position_document = {}
    for key, value in position.model_dump(by_alias=True).items():
        if key == "coordinates" and value is not None:
            position_document["location"] = value
        else:
            if value is not None:
                position_document[key] = value            

    # if there are one ore more attributes, update the student
    if len(position_document) >= 1: 
        
        update_result = await positions_collection.find_one_and_update(
            {"entity_id": entity_id},
            {"$set": position_document},
            return_document=True
        )

        if update_result is not None:
            return update_result
        else:
            return None

    # if there are no changed attributes, return already existing position
    if (existing_position := await positions_collection.find_one({"entity_id": entity_id})) is not None:
        return existing_position
    else:
        return None

async def modify_position_by_id(position_id: str, position: UpdatePositionSnapshot):
    # encapsulates coords in GeoJSON object if it is present
    if position.coordinates is not None:
        coords = position.coordinates
        position.coordinates = GeoJSONLocation(coordinates=coords)

    # create document (dict) from given position, only store values that are not null
    position_document = {}
    for key, value in position.model_dump(by_alias=True).items():
        if key is "coordinates":  
            if value is not None:
                position_document["location"] = value
        else:
            if value is not None:
                position_document[key] = value              

    # if there are one ore more attributes, update the student
    if len(position_document) >= 1: 
        
        update_result = await positions_collection.find_one_and_update(
            {"_id": ObjectId(position_id)},
            {"$set": position_document},
            return_document=True
        )

        if update_result is not None:
            return update_result
        else:
            return None

    # if there are no changed attributes, return already existing position
    if (existing_position := await positions_collection.find_one({"_id": position_id})) is not None:
        return existing_position
    else:
        return None
    
async def delete_position(position_id: str):

    delete_result = await positions_collection.delete_one({"_id": ObjectId(position_id)})

    if delete_result.deleted_count == 1:
        return True
    else:
        return False
    

# additional database functions:

async def insert_all(positions: list[PositionSnapshotDocument]):
    
    position_documents = [position.model_dump(by_alias=True, exclude="_id") for position in positions]
    result = await positions_collection.insert_many(position_documents)

    return result.inserted_ids
    

async def delete_all():

    document_count = await positions_collection.count_documents({})
    delete_results = await positions_collection.delete_many({})

    return document_count