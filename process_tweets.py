import os
import re
import time
import logging
from dotenv import load_dotenv
from openai import generate_response
from langchain.chat_models import ChatOpenAI
from twitter import TweetQueue, Tweet, Boolean

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# set up logging to file
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
    filename="twitter-bot.log",
    filemode="w",
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


def generate_tweets(llm: ChatOpenAI, tweetQueue: TweetQueue):
    for quant_tweet_idea in tweetQueue.tweets_not_sent:
        logging.info(5 * "*" + "Tweet to Gen" + 5 * "*")
        logging.info(quant_tweet_idea)
        first_response, short_response = generate_response(
            llm, quant_topic=quant_tweet_idea.topic, quant_title=quant_tweet_idea.title
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

        if count_length(first_draft) < 280:
            quant_tweet_idea.tweet = Tweet.from_dict(first_draft)
            quant_tweet_idea.gen_status = Boolean.TRUE

        elif count_length(short_response) < 280:
            quant_tweet_idea.tweet = Tweet.from_dict(short_response)
            quant_tweet_idea.gen_status = Boolean.TRUE

        else:
            logging.info("Value issue with Tweet")

        logging.info(50 * "-")
        time.sleep(30)


if __name__ == "__main__":
    # First step is to import file of topics and ides into TweetQueue
    tweetQueue = TweetQueue.from_text_file("quants_tweets.txt")

    llm = ChatOpenAI(
        temperature=0.3,
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-3.5-turbo-0613",
    )

    generate_tweets(llm, tweetQueue)

    tweetQueue.to_text_file("quants_tweets.txt")
