# Create a function that will call reddit api to pull the latest posts from it
# and then pull the title, url and text from the reddit post

# Import the required libraries
import praw
import os
import dotenv
from enum import Enum

dotenv.load_dotenv()

class RedditPostType(Enum):
    HOT = "hot"
    NEW = "new"
    CONTROVERSIAL = "controversial"


def init_praw():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    username = os.getenv("REDDIT_USERNAME")
    password = os.getenv("REDDIT_PASSWORD")
    # Create a reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=f"u/{username}",
        username=username,
        password=password,
    )
    return reddit

# Define a function to get the latest posts from a subreddit
def get_reddit_posts(reddit_client, subreddit_name: str, limit=5, post_type: RedditPostType = RedditPostType.HOT):

    # Get the subreddit
    subreddit = reddit_client.subreddit(subreddit_name)
    # Depending on type, get subreddit.hot or subreddit.new or subreddit.controversial
    if post_type == RedditPostType.HOT:
        posts = subreddit.hot(limit=limit)
    elif post_type == RedditPostType.NEW:
        posts = subreddit.new(limit=limit)
    elif post_type == RedditPostType.CONTROVERSIAL:
        posts = subreddit.controversial(limit=limit)
    else:
        raise ValueError("Invalid RedditPostType")
    # Create a list to store the posts
    data = []
    # Loop through the posts
    for post in posts:
        # Get the title, url and text of the post
        title = post.title
        url = post.url
        text = post.selftext

        # Create a dictionary to store the data
        post_data = {"title": title, "url": url, "text": text}
        # Append the data to the list
        data.append(post_data)

    return data

