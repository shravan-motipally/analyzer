import pymongo
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load the environment variables
load_dotenv()

MONGO_REDDIT_COLLECTION = os.getenv("MONGO_REDDIT_COLLECTION")
MONGO_TICKERS_COLLECTION = os.getenv("MONGO_TICKERS_COLLECTION")


class Mongo:
    def __init__(self):
        # Define the MongoDB connection
        mongo_uri = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB")
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[mongo_db]

    # Define a method to pull all tickers from the tickers collection
    def get_tickers(self):
        # Get the tickers collection
        tickers_collection = self.db[MONGO_TICKERS_COLLECTION]
        # Get the ticker and name attributes from each item in the tickers collection
        tickers = tickers_collection.find({}, {"ticker": 1, "name": 1, "_id": 0})

        # Extract the ticker attribute from each item in the collection and add it to a list and then return the list
        all_attributes = [(ticker["ticker"], ticker["name"]) for ticker in tickers]
        return all_attributes

    # Define a method to get reddit posts in mongo db filtered by those from the finance subreddit
    # from the last 24 hours
    def get_latest_reddit_posts(self, subreddit, hours=24):
        # Get the reddit collection
        reddit_collection = self.db[MONGO_REDDIT_COLLECTION]
        # Get the current time
        current_time = datetime.now()
        # Get the time 24 hours ago
        time_24_hours_ago = current_time - timedelta(hours=hours)
        # Get the finance posts from the last 24 hours
        finance_posts = reddit_collection.find(
            {
                "subreddit": subreddit,
                # "created_date": {"$gte": time_24_hours_ago.timestamp()},
            }
        )
        return finance_posts

    # define a method to push reddit posts to mongo db
    def push_reddit_posts(self, posts):
        # Get the reddit collection
        reddit_collection = self.db[MONGO_REDDIT_COLLECTION]
        # Insert the posts into the database
        for post in posts:
            try:
                if not reddit_collection.find_one({"id": post["id"]}):
                    print(f"Inserting post: {post['id']}")
                    post["created_date"] = datetime.now()
                    post["updated_date"] = datetime.now()
                    reddit_collection.insert_one(post)
                else:
                    # update the post
                    post["updated_date"] = datetime.now()
                    reddit_collection.update_one({"id": post["id"]}, {"$set": post})
            except Exception as e:
                print(f"Error inserting posts: {e}")
                raise e
