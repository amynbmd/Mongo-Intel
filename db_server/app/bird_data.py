import csv
import pymongo
from datetime import datetime
from collections import defaultdict
from pydantic import BaseModel
from math import sin, cos, sqrt, atan2, radians, degrees

class GeoJSONLocation(BaseModel):
    type: str = "Point"
    coordinates: tuple[float, float]    # format must be [longitude, latitude]

# data model formatted to be inserted into database
class PositionSnapshot(BaseModel):
    entity_id: int                      # entity id field specific to entity (see description in PositionSnapshot)
    name: str
    description: str | None = None
    location: GeoJSONLocation
    elevation: float | None = None      # (see description in PositionSnapshot)
    timestamp: datetime
    heading: float
    speed: float
    

# source: https://gis.stackexchange.com/questions/368559/techniques-for-point-level-speed-calculation-from-gps-traces
def lat_long_dist(lat1, lon1, lat2, lon2):
    # function for calculating ground distance between two lat-long locations
    R = 6373.0 # approximate radius of earth in km. 
    lat1 = radians( float(lat1) )
    lon1 = radians( float(lon1) )
    lat2 = radians( float(lat2) )
    lon2 = radians( float(lon2) )
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = round(R * c, 6)

    distance *= 1000    # convert km to m

    return distance


# source: https://gist.github.com/jeromer/2005586
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def calculate_heading(p1: dict, p2: dict) -> float:
    point1 = float(p1['location-lat']), float(p1['location-long'])
    point2 = float(p2['location-lat']), float(p2['location-long'])
    bearing = calculate_initial_compass_bearing(point1, point2)
    
    # print(f"{bearing=}")
    return bearing


# in m/s
def calculate_speed(p1: dict, p2: dict) -> int:
    t1 = datetime.strptime(p1['timestamp'], '%Y-%m-%d %H:%M:%S.000')
    t2 = datetime.strptime(p2['timestamp'], '%Y-%m-%d %H:%M:%S.000')
    time = (t2 - t1).total_seconds()

    lat1, long1 = p1['location-lat'], p1['location-long']
    lat2, long2 = p2['location-lat'], p2['location-long']
    distance = lat_long_dist(lat1, long1, lat2, long2)

    # print(f"{distance=}, \t{time=}, \t{distance/time=}")
    return distance/time


def csv_to_documents(
        filename: str, 
        entity_name: str, 
        entity_description: str, 
        id_field: str, 
        lat_field: str, 
        lon_field: str,
        height_field: str,
        timestamp_field: str,
        timestamp_format: str) -> list[PositionSnapshot]:
    
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)

        data = []
        for row in csvreader:
            data.append(row)

        # group by individual local identifier
        entities = defaultdict(list)
        for row in data:
            entities[row[id_field]].append(row)

        # create PositionSnapshot from extracted fields
        documents = []
        for identifier in entities:
            entity_history = entities[identifier]
            
            current_point = entity_history[0]
            for i in range(1, len(entity_history)):
                next_point = entity_history[i]

                
                current_point_doc = PositionSnapshot(
                    entity_id=int(identifier),
                    name=entity_name,
                    description=entity_description,
                    location=GeoJSONLocation(coordinates=(current_point[lon_field],current_point[lat_field])),
                    elevation=int(float(current_point[height_field])),
                    timestamp=datetime.strptime(current_point[timestamp_field], timestamp_format),
                    heading=calculate_heading(current_point, next_point),
                    speed=calculate_speed(current_point, next_point)
                )

                documents.append(current_point_doc)
                current_point = next_point 
            
        return documents


def upload_documents(documents: list[PositionSnapshot]):
    client = pymongo.MongoClient()
    db = client["mongo-intel"]
    collection = db["positions"]
    
    position_documents = [position.model_dump() for position in documents]
    result = collection.insert_many(position_documents)

    return result.inserted_ids

                
if __name__ == "__main__":
    
    documents = csv_to_documents(
        filename="GPS_tracking_of_eastern_whip-poor-will.csv",
        entity_name="Bird",
        entity_description="Flying bird",
        id_field="individual-local-identifier",
        lat_field="location-lat",
        lon_field="location-long",
        height_field="height-above-ellipsoid",
        timestamp_field="timestamp",
        timestamp_format="%Y-%m-%d %H:%M:%S.000"
    )

    inserted_ids = upload_documents(documents)
    print(inserted_ids)
    print(f"Inserted {len(inserted_ids)} documents")