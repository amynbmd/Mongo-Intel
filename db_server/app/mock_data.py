import mongo_db
import sys
import pprint

from mongo_db import PositionSnapshotDocument, GeoJSONLocation
from datetime import datetime, date, time

gmu = PositionSnapshotDocument(
    name='GMU',
    entity_id=0,
    description='George Mason University',
    location=GeoJSONLocation(type='Point', coordinates=[38.83178661625045, -77.31172257261196]),
    timestamp= datetime.combine(date(2023,10,28), time(10,00)),
    heading= 96.0,
    speed=35
)

car1 = PositionSnapshotDocument(
    name='Car',
    entity_id=1,
    description='Moving land vehicle',
    location=GeoJSONLocation(type='Point', coordinates=[38.83004244546952, -77.32488527067372]),
    timestamp=datetime.combine(date(2023,10,3), time(9,00)),
    heading= 96.0,
    speed=41
)

car2 = PositionSnapshotDocument(
    name='Car',
    entity_id=1,
    description='Moving land vehicle',
    location=GeoJSONLocation(type='Point', coordinates=[38.8639020490705, -77.33537283452927]),
    timestamp=datetime.combine(date(2023,10,3), time(9,30)),
    heading= 97.0,
    speed=45
)

car3 = PositionSnapshotDocument(
    name='Car',
    entity_id=1,
    description='Moving land vehicle',
    location=GeoJSONLocation(type='Point', coordinates=[38.873131614078076, -77.2891009266166]),
    timestamp=datetime.combine(date(2023,10,3), time(10,00)),
    heading= 98.0,
    speed=37
)

plane = PositionSnapshotDocument(
    name='Plane',
    entity_id=2,
    description='Moving air vehicle',
    location=GeoJSONLocation(type='Point', coordinates=[38.94109731258558, -77.4384997757568]),
    timestamp=datetime.combine(date(2023,10,2), time(11,00)),
    heading= 180,
    speed=280
)

position_data = [gmu, car1, car2, car3, plane,]  # <-- data that is uploaded to the database (feel free to play around with it)



async def clear_data():
    print('Clearing database...')
    deleted_count = await mongo_db.delete_all()
    print(f"Deleted {deleted_count} documents")


async def upload_data():
    print('Uploading mock data to database...')
    insertion_ids = await mongo_db.insert_all(position_data)
    print(f"Inserted {len(insertion_ids)} new documents")
    print(f"Insertion ids: {insertion_ids}")


async def show_data():
    print('Displaying database...')
    collection = await mongo_db.all_positions()
    for document in collection:
        pprint.pprint(document)


# if this file is run directly, run the function specified by the command line argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Correct usage is 'python mock_data.py [OPTION]'")
        print("Available options: 'clear', 'upload', 'show' ")
        exit()

    # option is given my command line argument, see README.md
    option = sys.argv[1]
    if option == 'clear':
        action = clear_data()
    elif option == 'upload':
        action = upload_data()
    elif option == 'show':
        action = show_data()
    else: 
        print(f"Option not recognized: '{option}'")
        print("Available options: 'clear', 'upload', 'show'")
        exit()    


    print()
    loop = mongo_db.client.get_io_loop()    # <-- ?? how to run async functions apparently (seen at "https://motor.readthedocs.io/en/stable/tutorial-asyncio.html")
    loop.run_until_complete(action)
    print()