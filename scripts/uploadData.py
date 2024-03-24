import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://xavier-souffront:0U5jY8WuzhIPOMSM@gcpcluster.rwcznai.mongodb.net/"

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))
                          
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


#####

mongoClient = MongoClient()
db = mongoClient['data_storage']
collection = db['bedBugData']
header = ['registration_id', 'building_id','borough',
'house_number','street_name', 'postcode',
'of_dwelling_units','infested_dwelling_unit_count', 'eradicated_unit_count',
're_infested_dwelling_unit','filing_date', 'filing_period_start_date',
'filling_period_end_date', 'latitude', 'longitude',
'community_board','city_council_district', 'census_tract_2010',
'bin','bbl','nta']

csvFile = open('/Users/16466/Desktop/cis4400Homework/scripts/bedBugData.csv','r')
reader = csv.DictReader(csvFile)

for x in reader:
    row = {}
    for field in header:
        row[field] = x[field]
    print(row)
    collection.insert_one(row)