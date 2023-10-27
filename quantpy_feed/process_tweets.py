import os
import re
import time
import logging
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

if __name__ == "__main__":
    # module being called directly, use absolute path
    from call_openai import generate_response
    from twitter import TweetQueue, Tweet, Boolean

else:
    # module being called as package, use relative paths
    from .call_openai import generate_response
    from .twitter import TweetQueue, Tweet, Boolean

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setting Variables
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
LOG_FILE = os.path.join(APP_DIR, "twitter-bot.log")
TEXT_FILE = os.path.join(APP_DIR, "data/processed/quants_tweets.txt")

# set up logging to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename=LOG_FILE,
    filemode="a",
)


count_length = lambda d: sum(len(d[val]) for val in d)
count_words = lambda d: sum(len(re.findall(r"\w+", d[val])) for val in d)
key_list = [
    "Hook",
    "Intro",
    "Explanation",
    "Application",
    "Closing",
    "Action",
    "Engagement",
]


def extract_tweet(openai_tweet: str, key_list: list) -> dict:
    """Creates dictionary from Openai response using keyword template

    Parameters:
        - openai_tweet:
        - key_list: list key words used for searching reponse template

    Returns:
        - dictionary: templated tweet
    """
    template = {}
    # Iterate through key list
    for i, key in enumerate(key_list):
        # find starting position
        start = openai_tweet.find(key_list[i]) + len(key_list[i]) + 2
        if i != len(key_list) - 1:
            # using ending position, subset str and append to template
            end = openai_tweet.find(key_list[i + 1])
            line = openai_tweet[start:end]
            template[key_list[i]] = line
        else:
            # if final word in list, only subsection by start word
            template[key_list[i]] = openai_tweet[start:]
    return template


def generate_tweets(llm: ChatOpenAI, tweetQueue: TweetQueue, text_file: str):
    for quant_tweet_track in tweetQueue.tweets_not_generated:
        logging.info(5 * "*" + "Tweet to Gen" + 5 * "*")
        logging.info(quant_tweet_track)
        first_response, short_response = generate_response(
            llm,
            quant_topic=quant_tweet_track.topic,
            quant_title=quant_tweet_track.title,
        )
        logging.info(5 * "*" + "First Draft" + 5 * "*")
        first_draft = extract_tweet(first_response, key_list)
        logging.info(
            f"Content Length: {count_length(first_draft)} Tweet Dict {first_draft}"
        )
        logging.info(5 * "*" + "Second Draft" + 5 * "*")
        short_response = extract_tweet(short_response, key_list)
        logging.info(
            f"Content Length: {count_length(short_response)} Tweet Dict {short_response}"
        )

        final_tweet = {}
        for key, val in first_draft.items():
            if len(val) < 280:
                final_tweet[key] = val

            elif len(short_response[key]) < 280:
                final_tweet[key] = short_response[key]

            else:
                final_tweet[key] = short_response[key][:270]
                logging.info(f"Value issue with Tweet {key}, too long")

        quant_tweet_track.tweet = Tweet.from_dict(final_tweet)
        quant_tweet_track.update_gen_status(Boolean.TRUE)

        tweetQueue.to_text_file(text_file)

        logging.info(50 * "-")
        time.sleep(25)


def search_next_tweet(tweetQueue: TweetQueue):
    if (
        len(tweetQueue.tweets_not_generated)
        == 0 & len(tweetQueue.tweets_ready_for_sending)
        == 0
    ):
        logging.warning(ValueError("Need to create more tweet data"))
        raise ValueError("Need to create more tweet data")
    else:
        tweetQueue.tweets.sort(reverse=False, key=lambda tweet: tweet.id)
        quant_tweet = tweetQueue.tweets_not_sent[0]
        return quant_tweet


if __name__ == "__main__":
    # First step is to import file of topics and ides into TweetQueue
    text_file = TEXT_FILE
    tweetQueue = TweetQueue.from_text_file(text_file)

    llm = ChatOpenAI(
        temperature=0.3,
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-3.5-turbo-0613",
    )

    generate_tweets(llm, tweetQueue, text_file)

    tweetQueue.to_text_file(text_file)
