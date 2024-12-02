import pymongo
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

class Mongo:
    def __init__(self):
        # Define the MongoDB connection
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB")
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[mongo_db]

    def insert_data(self, collection: str, data):
        try:
            # Get the collection
            collection = self.db[collection]
            # Insert the data
            collection.insert_one(data)
        except Exception as e:
            print(f"Error inserting data: {e}")
