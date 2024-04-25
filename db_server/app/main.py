from fastapi import FastAPI
from fastapi import HTTPException, Response, status 
from mongo_db import PositionSnapshot, PositionSnapshotDocument, PositionSnapshotCollection, UpdatePositionSnapshot
import mongo_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["http://localhost:3000"]  # List of allowed origins

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
async def root():
    return {
        "message": "Welcome to Mongo Intel database server", 
        "info": "navigate to '/docs' to view API endpoints" 
    }

# CRUD API endpoints:
@app.get(path='/positions', response_model=PositionSnapshotCollection)
async def list_positions(page: int = 0):
    collection = PositionSnapshotCollection(position_docs=await mongo_db.all_positions(page))
    return collection


@app.get(path='/positions/{entity_id}', response_model=PositionSnapshotDocument)
async def get_position(entity_id: int):
    position = await mongo_db.find_position(entity_id)

    if position is None:
        raise HTTPException(status_code=404, detail=f"Position with entity_id '{entity_id}' not found")
    else:
        return position

    
@app.post(path='/positions', response_model=PositionSnapshotDocument)
async def create_position(position: PositionSnapshot):
    print(position)
    created_position = await mongo_db.insert_position(position)
    return created_position

@app.put(path='/positions/{position_id}', response_model=PositionSnapshotDocument)
async def modify_position(position_id: str, new_position: UpdatePositionSnapshot):
    print(position_id)
    print(new_position)
    updated_position = await mongo_db.modify_position_by_id(position_id, new_position)
    
    if updated_position is None:
        raise HTTPException(status_code=404, detail=f"Position with id '{position_id}' not found")
    else:
        return updated_position

@app.delete('/positions/{position_id}')
async def delete_document(position_id: str):
    successful_deletion = await mongo_db.delete_position(position_id)
    
    if successful_deletion:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail=f"Position with id '{position_id}' not found")
    

@app.put(path='/entity-positions/{entity_id}', response_model=PositionSnapshotDocument)
async def modify_entity_position(entity_id: int, new_position: UpdatePositionSnapshot):
    updated_position = await mongo_db.modify_position(entity_id, new_position)
    
    if updated_position is None:
        raise HTTPException(status_code=404, detail=f"Position with id '{entity_id}' not found")
    else:
        return updated_position   