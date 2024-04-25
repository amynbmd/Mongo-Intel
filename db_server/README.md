# Mongo Intel Database Server

## Purpose
The database server functions as the way to perform CRUD (create, read, update, delete) operations of position data in the database. 

By separating the functions of `storing position data`, and `querying position data`, the app becomes more modular


## Structure
The `db-server/` directory contains an `app/` directory which holds the actual application, and a `requirements.txt` file which specifies the libraries needed to run the application

The `db-server/app/` directory contains the following files:
- Web server: `main.py`
- Database connection: `mongo_db.py`
- Mock data: `mock_data.py`


## Web Server Usage
0. Within the `db-server/` directory, install necessary libraries using command
`pip install -r requirements.txt`

1. Within the `db-server/app` directory, start the webserver using the command
`uvicorn main:app --reload --port 8001` or `python -m uvicorn main:app --reload --port 8001`


2. Navigate to URL `http://localhost:8001/docs` to view documentation on API endpoints


## Mock Data Usage
0. Within the `db-server/` directory, install necessary libraries using command
`pip install -r requirements.txt`

1. Within the `db-server/app` directory, you can perform operations on the mock data using any of the following commands
    * `python mock_data.py clear`  - remove all data from database
    * `python mock_data.py upload` - upload data to database
    * `python mock_data.py show`   - display data held in database