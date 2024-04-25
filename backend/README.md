# Mongo Intel Backend

## Purpose

The backend functions as the way for queries to be processed, computed, and predicted, so that the query results can be communicated back to the frontend client

## Structure

The `backend/` directory contains an `app/` directory which holds the actual application, and a `requirements.txt` file which specifies the libraries needed to run the application

The `backend/app/` directory contains all necessary modules of the project:

- Web server: `server.py`
- AI/ML processor: `ai.py`
- NLP processor: `nlp.py`[]
- Apache Solr search engine: `solr.py`

As well as extra files for necessary functions:

- Test application and functions: `test.py`
- Process and resolve queries: `query.py`
- Database schema definition: `mongo_db.py`
- NLP using nl2query model: `nl2query_model.py`
- NLP using spaCy model: `spacy_model.py`

## Web Server Usage

0. Within the `backend/` directory, install necessary libraries using command
   `pip install -r requirements.txt`
   `python3 -m spacy download en`

1. Within the `backend/app/` directory, start the webserver using the command
   `uvicorn server:app --reload` or `python -m uvicorn server:app --reload`

2. Navigate to URL `http://localhost:8000/docs` to view documentation on API endpoints

## Run tests

0. Within the `backend/` directory, install necessary libraries using command
   `pip install -r requirements.txt`

1. Within the `backend/app/` directory, run command
   `pytest test.py`

## Run queries

0. Within the `backend/` directory, install necessary libraries using command
   `pip install -r requirements.txt`

1. Within the `backend/app/` directory, run command
   `python query.py` to run the (hardcoded) query and view results

2. (OPTIONAL) change the hardcoded query by setting the 'query' variable to another one of the premade queries, or make your own query and add to it.
