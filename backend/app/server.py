# Webserver functionalities like API endpoints

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import the CORS middleware
from mongo_db import PositionSnapshot
from query import resolve_query, string_to_query
import nlp
from fastapi import Response
import requests
import datetime


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

# Add favicon.ico to avoid 404 error
@app.get("/favicon.ico")
async def get_favicon():
    return Response(content="", media_type="image/x-icon")

# Geocoding API endpoint
@app.get("/geocode")
async def geocode(address: str):
    # Use Google Geocoding API or another geocoding service
    response = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyADv-iUMeyp0rv9C4xBZG7cGyFpq0SEogk")
    data = response.json()
    if not data['results']:
        raise HTTPException(status_code=404, detail="Location not found")

    location = data['results'][0]['geometry']['location']
    return {"lat": location['lat'], "lng": location['lng']}

@app.get('/')
async def root():
    return {
        "message": "Welcome to Mongo Intel backend query server", 
        "info": "navigate to '/docs' to view API endpoints" 
    }


# Direct query route:
# -------------------
# take in MongoDB query as a string through the query params, 
# and return back the query results as a list of Position Snapshots (JSON objects)
# list will be empty if there are no results

# example URL: http://localhost:8000/direct?query={%22name%22:%22GMU%22}    <-- (%22 encodes " double quotes)
@app.get(path='/direct', response_model=list[PositionSnapshot])
async def direct_query(query: str, page: int = 0):
    mongo_query = string_to_query(query)
    if mongo_query is None:
        raise HTTPException(status_code=400, detail="Cannot parse query, must use MongoDB syntax (JSON)") 
    
    print(mongo_query)
    query_results = await resolve_query(mongo_query, page)
    return query_results


# NLP text query route:
# ---------------------
# take in natural language text as a string through the query params, 
# and return back the query results as a list of Position Snapshots (JSON objects)
# list will be empty if there are no results

# example URL: http://localhost:8000/nlp?text=Where%20is%20GMU  <-- (%20 encodes space character)
@app.get(path='/nlp', response_model=list[PositionSnapshot])
async def natural_language_query(text: str, page: int = 0):
    query = nlp.text_to_query(text)
    
    query_results = await resolve_query(query, page)
    return query_results


@app.get(path='/time', response_model=list[PositionSnapshot])
async def time_query(time: datetime.datetime, before: bool = True, page: int = 0):
    
    if before:
        query = {"timestamp": {"$lte": time}}
    else:
        query = {"timestamp": {"$gte": time}}

    query_results = await resolve_query(query, page)
    return query_results