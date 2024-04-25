# AI/ML functionalities
from motor import motor_asyncio
from pydantic import BaseModel, BeforeValidator, Field
from mongo_db import PositionSnapshot, GeoJSONLocation, query_positions, find_most_recent
from datetime import datetime, timedelta
from typing import Optional
from typing_extensions import Annotated
import pprint
import re

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score



PyObjectId = Annotated[str, BeforeValidator(str)]

client = motor_asyncio.AsyncIOMotorClient("192.168.1.46", 27017)
db = client.get_database("mongo-intel")
positions_collection = db.get_collection("positions")

class AI_Input:
    queries: list[dict]     # queries
    time_offset: timedelta  # 0 means present, + means future, - means past

    def __init__(self, queries, time_offset) -> None:
        self.queries = queries
        self.time_offset = time_offset


async def is_predictive_query(query: dict) -> bool:
    # timestamp is either a singe time or a range (dict), or it doesn't exist
    ts = query.get("timestamp")
    if ts == None:
        return False
    
    # get timestamp from dict if it is a range
    if type(ts) == dict:
        ts = ts.get("$gte")
    
    ts: datetime    # timestamp will definitely be a datetime by now
    most_recent_point: dict = await find_most_recent(query)
    if most_recent_point is not None and ts > most_recent_point["timestamp"]:
        print("Query is predictive!")
        return True
    else:
        print("Query is not predictive!")
        return False

def create_ai_input(query):
    timestamp: datetime = query.get("timestamp").get("$lt")
    
    time_offset: timedelta = timestamp - datetime.utcnow()
    query["timestamp"] = {"$lt": query.get("timestamp").get("$gte")}
    ai_input = AI_Input([query], time_offset)
    return ai_input


def possible_implementation(queries: list[dict], offset: timedelta) -> list[PositionSnapshot]:
    
    total_docs = []
    for query in queries:
        # documents = db.find(query)    # retrieve PositionSnapshots
        # total_docs += documents
        ...

    # result = extrapolate_position(total_docs, offset)
    
    return []



async def predict(input: AI_Input) -> list[PositionSnapshot]:
    query_results = []
    
    queries = input.queries

    # instructions = [
    total_docs = []    
    
    for query in queries:
        documents = positions_collection.find(query)
        total_docs.append(await documents.to_list(100))

    snapshots_np = []
    for x in total_docs:
        for y in x:
            snapshots_np.append(y)
            
    print(snapshots_np)
    
    query_results = model(snapshots_np, query)
    
    return query_results


def model(snapshots_np: list, query) -> PositionSnapshot:
    object_pred_df = pd.DataFrame()
    counter = 0
    for x in snapshots_np:
        for y in x:
            x[y] = [x.get(y)]
        if counter == 0:
            object_pred_df = pd.DataFrame(x)
            counter += 1
            continue
        object_pred_df = pd.concat([object_pred_df, pd.DataFrame(x, index=[counter,])])
        counter += 1
            
    end_entity_id = object_pred_df.at[0, 'entity_id']
    
    #Parse Date
    counter = 0
    for x in object_pred_df['timestamp']:
        parsed_date_e = []

        parsed_date_e.append(x.year)
        parsed_date_e.append(x.month)
        parsed_date_e.append(x.day)
        parsed_date_e.append(x.hour)
        parsed_date_e.append(x.minute)
        parsed_date_e.append(x.second)
        parsed_date_e.append(x.microsecond)

        object_pred_df.at[counter, 'year'] = int(parsed_date_e[0])
        object_pred_df.at[counter, 'month'] = int(parsed_date_e[1])
        object_pred_df.at[counter, 'day'] = int(parsed_date_e[2])
        object_pred_df.at[counter, 'hour'] = int(parsed_date_e[3])
        object_pred_df.at[counter, 'minute'] = int(parsed_date_e[4])
        object_pred_df.at[counter, 'second'] = int(parsed_date_e[5])
        object_pred_df.at[counter, 'microsecond'] = int(parsed_date_e[6])
        counter += 1
    
    counter = 0
    for x in object_pred_df['location']:
        coordinates = x.get('coordinates')
        lat = coordinates[1]
        lon = coordinates[0]  
        
        object_pred_df.at[counter, 'lat'] = lat
        object_pred_df.at[counter, 'lon'] = lon
        counter += 1
    
    
    object_pred_df.sort_values(by=['timestamp'], inplace=True)
    object_pred_df.drop(columns=['_id', 'entity_id', 'name', 'description', 'location', 'timestamp'], inplace=True)
    
    
    for (columnName, columnData) in object_pred_df.items():
        object_pred_df[columnName] = columnData.replace({None: np.nan})
        object_pred_df[columnName].fillna(0, inplace=True)
    
    

    x = object_pred_df.drop(columns=['lat', 'lon'])
    y = object_pred_df.drop(columns=['elevation', 'heading', 'speed', 'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond'])

    X_train, X_test, Y_train, Y_test =  train_test_split(x, y, test_size=0.1, random_state=4)

    greg = RandomForestRegressor(min_samples_leaf=2, n_estimators=415, random_state=1)
    greg.fit(X_train, Y_train)
    
    for y in query:
            query[y] = [query.get(y)]
    predict_question = pd.DataFrame(query)
    
    counter = 0
    predict_timestamp = query['timestamp'][0].get("$lt")
    parsed_date_e = []
    parsed_date_e.append(predict_timestamp.year)
    parsed_date_e.append(predict_timestamp.month)
    parsed_date_e.append(predict_timestamp.day)
    parsed_date_e.append(predict_timestamp.hour)
    parsed_date_e.append(predict_timestamp.minute)
    parsed_date_e.append(predict_timestamp.second)
    parsed_date_e.append(predict_timestamp.microsecond)

    predict_question.at[counter, 'elevation'] = 0
    predict_question.at[counter, 'heading'] = 0
    predict_question.at[counter, 'speed'] = 0
    predict_question.at[counter, 'year'] = int(parsed_date_e[0])
    predict_question.at[counter, 'month'] = int(parsed_date_e[1])
    predict_question.at[counter, 'day'] = int(parsed_date_e[2])
    predict_question.at[counter, 'hour'] = int(parsed_date_e[3])
    predict_question.at[counter, 'minute'] = int(parsed_date_e[4])
    predict_question.at[counter, 'second'] = int(parsed_date_e[5])
    predict_question.at[counter, 'microsecond'] = int(parsed_date_e[6])
    
    predict_question.drop(columns=['name', 'timestamp'], inplace=True)

    y_pred = greg.predict(predict_question)
    
    print(X_test.head())
    print(y_pred)
    
    # og_mae = mean_absolute_error(y_pred, Y_test)

    # og_mse = mean_squared_error(y_pred, Y_test)
    
    # print("stats:")
    # print("MAE:", og_mae)
    # print("MSE:", og_mse)
    
    pred_point = GeoJSONLocation(type='Point', coordinates=[y_pred[0][1], y_pred[0][0]])
        
    predict_dict = {'entity_id': end_entity_id, 'description': "Predicted location", 'name': query['name'][0], 'location': pred_point, 'timestamp': predict_timestamp, 'heading': 0, 'speed': 0}
    predict_results = [predict_dict]
    
    ##Make it so that the Entered data is in the correct format, as right now there are just json objects being pased into the df and not the appropriate columns
    
    return predict_results