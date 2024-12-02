# Import all the libraries required for the code to run
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from external.reddit import init_praw, get_reddit_posts, RedditPostType
from hf.finbert import Finbert


def analyze_positive_or_negative_sentiment(text):
    # Create a sentiment analyzer
    sentiment = SentimentIntensityAnalyzer()
    # Get the sentiment score
    score = sentiment.polarity_scores(text)
    # Get the compound score
    compound_score = score["compound"]
    # Check if the compound score is positive
    return compound_score


# use the finbert model to analyze the sentiment of the text
def analyze_finbert(text):
    # Create an instance of the Finbert class
    finbert = Finbert()
    # Get the sentiment of the text
    sentiment = finbert.predict(text)
    return sentiment


# Create a main function to call the sentiment analyzer
def main():
    # Initialize praw
    reddit_client = init_praw()
    # Get the latest posts from the subreddit
    posts = get_reddit_posts(reddit_client, "finance", limit=5, post_type=RedditPostType.HOT)

    # For each title in the posts, let's analyze the sentiment and assign an attribute called "sentiment" to it
    for post in posts:
        title = post["title"]
        post["pn_sentiment"] = analyze_positive_or_negative_sentiment(title)

        post["finbert_sentiment"] = analyze_finbert(title)
        # now print the title along with both sentiments
        print(f"Title: {title}, PN Sentiment: {post['pn_sentiment']}, Finbert Sentiment: {post['finbert_sentiment']}")

# Call the main function
if __name__ == "__main__":
    main()
