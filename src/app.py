# Import all the libraries required for the code to run
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from db.mongo import Mongo
from hf.finbert import Finbert
from hf.fin_news_sentiment_analysis import FinNewsSentimentAnalysis
from hf.finsummary import FinSummary
from ner.spacy_ner import extract_entities
from util.fuzzy_similarity import is_extremely_similar
from util.cosine_similarity import is_extremely_similar_cosine
from util.email_client import inform_user_of_latest_posts


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
def analyze_financial_sentiment(text):
    # Create an instance of the Finbert class
    finbert = Finbert()
    # Get the sentiment of the text
    sentiment = finbert.predict(text)
    return sentiment


# use the finnews model to analyze the sentiment of the text
def analyze_financial_news_sentiment(text):
    # Create an instance of the FinNewsSentimentAnalysis class
    finnews = FinNewsSentimentAnalysis()
    # Get the sentiment of the text
    sentiment = finnews.predict(text)
    return sentiment


# use the finsummary model to summarize the text
def summarize_financial_text(text):
    # Create an instance of the FinSummary class
    finsummary = FinSummary()
    # Get the summary of the text
    summary = finsummary.summarize(text)
    return summary


# use space_ner to extract the entities from the text
def extract_named_entities_within_financial_text(text, mongo: Mongo):
    # Extract the named entities from the text
    entities = extract_entities(text)

    tickers = []
    all_tickers_symbol_and_names = mongo.get_tickers()

    all_tickers = [tik_tuple[0] for tik_tuple in all_tickers_symbol_and_names]
    all_names = [tik_tuple[1] for tik_tuple in all_tickers_symbol_and_names]
    for idx in range(len(entities)):
        entity = entities[idx]
        print(f"Checking entity: {entity}")
        if entity in all_tickers:
            print(f"Found ticker: {entity}" in all_tickers)
            tickers.append(entity)
        elif entity in all_names:
            print(f"Found name: {entity}" in all_names)
            tickers.append(all_tickers[all_names.index(entity)])
        else:
            # TODO - make this more efficient
            for ticker, name in all_tickers_symbol_and_names:
                print(f"Checking similarity between {entity} and {name}")
                if is_extremely_similar_cosine(entity, name):
                    tickers.append(ticker)
                    break

    return tickers


# Create a main function to call the sentiment analyzer
def main():

    # Create an instance of the Mongo class
    mongo = Mongo()

    # Get the last 24 hours of the finance subreddit
    posts = mongo.get_latest_reddit_posts("wallstreetbets", hours=24)

    total_posts_found = len(list(posts.clone()))
    print(f"{total_posts_found} posts found")

    # For each title in the posts, let's analyze the sentiment and assign an attribute called "sentiment" to it
    for post in posts:
        title = post["title"]
        text = post["text"]
        post["title_pn_sentiment"] = analyze_positive_or_negative_sentiment(title)
        post["title_finbert_sentiment"] = analyze_financial_sentiment(title)
        post["title_finnews_sentiment"] = analyze_financial_news_sentiment(title)

        post["text_pn_sentiment"] = (
            analyze_positive_or_negative_sentiment(text) if text else None
        )
        # post["text_summary"] = summarize_financial_text(text) if text else None
        post["text_finnews_sentiment"] = (
            analyze_financial_news_sentiment(text) if text else None
        )

        post["title_entities"] = extract_named_entities_within_financial_text(
            title, mongo
        )
        post["text_entities"] = (
            extract_named_entities_within_financial_text(text, mongo) if text else None
        )

        # now print the text and title along with all the attributes
        print(f"Title: {title}")
        print(f"Text: {text}")
        print(f"Title Positive/Negative Sentiment: {post['title_pn_sentiment']}")
        print(f"Title Finbert Sentiment: {post['title_finbert_sentiment']}")
        print(f"Title FinNews Sentiment: {post['title_finnews_sentiment']}")
        print(f"Text Positive/Negative Sentiment: {post['text_pn_sentiment']}")
        # print(f"Text Summary: {post['text_summary']}")
        print(f"Text FinNews Sentiment: {post['text_finnews_sentiment']}")
        print(f"Title Entities: {post['title_entities']}")
        print(f"Text Entities: {post['text_entities']}")

        # push post to mongo
        mongo.push_reddit_posts([post])

    # Now for each post in the reddit collectio that has title_entities or text_entities that are not an empty array, let's collate them and send them in an email
    # to numtheory@ymail.com

    # First let's pull all the posts that have title_entities or text_entities that are not an empty array
    posts_with_entities = mongo.get_latest_reddit_posts("wallstreetbets", hours=24)
    posts_with_entities = [
        post
        for post in posts_with_entities
        if post["title_entities"] or post["text_entities"]
    ]

    # Then let's send the email
    inform_user_of_latest_posts(posts_with_entities, "wallstreetbets")


# Call the main function
if __name__ == "__main__":
    main()
