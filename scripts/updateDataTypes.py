from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://xavier-souffront:0U5jY8WuzhIPOMSM@gcpcluster.rwcznai.mongodb.net/"

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['data_storage']
collection = db['bedBugData']                    

# Update data types for specified columns
update_columns = {
    'of_dwelling_units': int,
    'infested_dwelling_unit_count': int,
    'eradicated_unit_count': int,
    're_infested_dwelling_unit': int,
    'latitude': float,
    'longitude': float,
    'filing_date': lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'),
    'filing_period_start_date': lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f'),
    'filling_period_end_date': lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
}

for column, data_type in update_columns.items():
    # Iterate over documents and update each one
    for document in collection.find({column: {"$exists": True}}):
        value = document[column]
        if isinstance(value, str):
            new_value = data_type(value)
            collection.update_one({"_id": document["_id"]}, {"$set": {column: new_value}})
        else:
            print(f"Skipping update for {column} for document with _id {document['_id']}: Value is not a string")

# Confirm the updates
updated_docs = collection.find({}, {column: 1 for column in update_columns.keys()})

for doc in updated_docs:
    print(doc)