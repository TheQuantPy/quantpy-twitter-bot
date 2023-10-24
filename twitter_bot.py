import os
import tweepy
import logging
from dataclasses import asdict
from langchain.chat_models import ChatOpenAI
from quantpy_feed.twitter import Boolean, Tweet, TweetType, TweetQueue
from quantpy_feed.process_tweets import generate_tweets, search_next_tweet

# Helpful when testing locally
from dotenv import load_dotenv
load_dotenv()

# Setting Variables
TWEET_TYPE = TweetType.THREAD
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_FILE = os.path.join(CUR_DIR, 'data/processed/quants_tweets.txt')

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
    filemode="a",
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

        self.text_file = TEXT_FILE

        self.tweetQueue = TweetQueue.from_text_file(self.text_file)

    def verify_tweet_to_send(self) -> None:
        if len(self.tweetQueue.tweets_ready_for_sending) == 0:
            self.process_tweets()

    def process_tweets(self):
        generate_tweets(self.llm, self.tweetQueue)
        self.tweetQueue.to_text_file(self.text_file)
        
    def reply_tweet(self, original_tweet_id: int, tweet_reply: str) -> None:
        self.twitter_api.update_status(status=tweet_reply, 
                                    in_reply_to_status_id=original_tweet_id, 
                                    auto_populate_reply_metadata=True)
        
    def post_thread(self, tweet: Tweet) -> None:
        tweet_d = asdict(tweet)
        try:
            for key, tweet_thread in tweet_d.items():
                if key == 'Hook':
                    _tweet_thread = self.twitter_api.create_tweet(text=tweet_thread)
                else:
                    self.twitter_api.create_tweet(
                                    text=tweet_thread,
                                    in_reply_to_tweet_id=_last_tweet_id.data['id']
                                    )
                _last_tweet_id = _tweet_thread
                logging.info('Sent Status: TRUE. Tweet: {tweet_thread}')
            return True
        except Exception as e:
            logging.warning(e)
            return False

    def post_tweet(self, tweet: Tweet) -> None:
        quant_tweet = tweet.to_text()
        try:
            self.twitter_api.create_tweet(text=quant_tweet)
            logging.info('Sent Status: TRUE. Tweet: {quant_tweet}')
            return True
        except Exception as e:
            logging.warning(e)
            return False
        
    def save_file(self):
        self.tweetQueue.to_text_file(self.text_file)
        logging.info("Latest version of tweets saved down.")

def run_quantpy_feed_bot():
    # First step is to import file of topics and ides into TweetQueue
    twitterBot = TwitterBot()
    # ensure there are tweets to send
    twitterBot.verify_tweet_to_send()
    # Identify Tweet Track to Send
    quant_track = search_next_tweet(twitterBot.tweetQueue)
    # post single tweet
    if TWEET_TYPE == TweetType.SINGLE:
        if twitterBot.post_tweet(tweet = quant_track.tweet):
            quant_track.sent_status = Boolean.TRUE
    # post tweet thread
    elif TWEET_TYPE == TweetType.THREAD:
        if twitterBot.post_thread(tweet = quant_track.tweet):
            quant_track.sent_status = Boolean.TRUE
    # save down file
    twitterBot.save_file()

if __name__ == "__main__":
    run_quantpy_feed_bot()

