import os
import tweepy
import logging
from dataclasses import dataclass, asdict
from twitter import Tweet, TweetQueue
from langchain.chat_models import ChatOpenAI

# import generate_tweet
from process_tweets import generate_tweets, search_next_tweet

# Helpful when testing locally
from dotenv import load_dotenv
load_dotenv()

# Load your Twitter and Airtable API keys (preferably from environment variables, config file, or within the railyway app)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# set up logging to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename="twitter-bot.log",
    filemode="w",
)

# TwitterBot class to help us organize our code and manage shared state
class TwitterBot:
    def __init__(self):
        self.twitter_api = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN,
                                         consumer_key=TWITTER_API_KEY,
                                         consumer_secret=TWITTER_API_SECRET,
                                         access_token=TWITTER_ACCESS_TOKEN,
                                         access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                                         wait_on_rate_limit=True)

        self.llm = ChatOpenAI(
            temperature=0.3,
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo-0613",
        )

        self.text_file = "quants_tweets.txt"

        self.tweetQueue = TweetQueue.from_text_file(self.text_file)

    def process_tweets(self):
        generate_tweets(self.llm, self.tweetQueue)
        self.tweetQueue.to_text_file(self.text_file)
        
    def reply_tweet(self, original_tweet_id: int, tweet_reply: str) -> None:
        self.twitter_api.update_status(status=tweet_reply, 
                                    in_reply_to_status_id=original_tweet_id, 
                                    auto_populate_reply_metadata=True)
        
    def post_thread(self, tweet: Tweet) -> None:
        tweet_d = asdict(tweet)
        for key, tweet_thread in tweet_d.items():
            if key == 'Hook':
                _tweet_thread = self.twitter_api.update_status(status=tweet_thread)
            else:
                self.reply_tweet(original_tweet_id=_last_tweet_id.id,
                                 tweet_reply=tweet_thread)

            _last_tweet_id = _tweet_thread

    def post_tweet(self) -> None:
        if len(self.tweetQueue.tweets_ready_for_sending) == 0:
            self.process_tweets()

        quant_track = search_next_tweet(self.tweetQueue)
        quant_tweet = quant_track.tweet.to_text()
        print(quant_tweet)
        try:
            response_tweet = self.twitter_api.create_tweet(text=quant_tweet)
        except Exception as e:
            logging.warning(e)

if __name__ == "__main__":
    # First step is to import file of topics and ides into TweetQueue
    twitterBot = TwitterBot()
    # twitterBot.process_tweets()
    twitterBot.post_tweet()