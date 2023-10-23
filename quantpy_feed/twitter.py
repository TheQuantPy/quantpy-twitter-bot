from enum import Flag, auto
from json import dumps, loads
from dataclasses import dataclass, asdict, field

class Boolean(Flag):
    TRUE = True
    FALSE = False

class TweetType(Flag):
    SINGLE = auto()
    THREAD = auto()

@dataclass
class Tweet:
    Hook: str
    Intro: str
    Explanation: str
    Application: str
    Closing: str
    Action: str
    Engagement: str

    @classmethod
    def from_dict(cls, tweet_d: dict):
        # return class
        return cls(
            Hook=tweet_d["Hook"],
            Intro=tweet_d["Intro"],
            Explanation=tweet_d["Explanation"],
            Application=tweet_d["Application"],
            Closing=tweet_d["Closing"],
            Action=tweet_d["Action"],
            Engagement=tweet_d["Engagement"],
        )
    
    def to_text(self):
        _spaced_response = f"{self.Hook}\n{self.Intro}\n{self.Explanation}\n{self.Application}\n{self.Closing}\n{self.Action}\n{self.Engagement}"
        if len(_spaced_response) > 280:
            return f"{self.Hook}{self.Intro}{self.Explanation}{self.Application}{self.Closing}{self.Action}{self.Engagement}"
        else:
            return _spaced_response


@dataclass
class TrackTweet:
    """Class for keeping track of Tweets"""

    id: int
    topic: str
    title: str
    sent_status: Boolean = Boolean.FALSE
    gen_status: Boolean = Boolean.FALSE
    tweet: Tweet = field(init=False, repr=False)

    def __lt__(self, other):
        return (self.sent_status.value, self.id) < (other.sent_status.value, other.id)

    @classmethod
    def from_str(cls, tweet_line: str):
        # underscores used to indicate unpacked variables, only used internally
        (
            _id,
            _topic,
            _title,
            _sent_status,
            _gen_status,
            _tweet,
            _next_line,
        ) = tweet_line.split("|")
        # convert status TRUE/FALSE to Enum Representation
        _sent_status_bool = (
            Boolean.TRUE if _sent_status == Boolean.TRUE.name else Boolean.FALSE
        )
        # confirm if tweet already written or not, if so load previously written tweet
        _gen_status_bool = (
            Boolean.TRUE if _gen_status == Boolean.TRUE.name else Boolean.FALSE
        )
        # init class without tweet
        _trackTweet = cls(
            id=int(_id),
            topic=_topic,
            title=_title,
            sent_status=_sent_status_bool,
            gen_status=_gen_status_bool,
        )

        if _gen_status_bool:
            # return class with written tweet
            _trackTweet.tweet = Tweet.from_dict(loads(_tweet))

        return _trackTweet

    def to_str(self):
        _part_1 = f"{self.id}|{self.topic}|{self.title}|{self.sent_status.name}|{self.gen_status.name}|"
        _part_2 = (
            f"{dumps(asdict(self.tweet)) if hasattr(self, 'tweet') else 'FALSE'}|\n"
        )
        return _part_1 + _part_2

    def update_status(self, new_status: Boolean):
        self.sent_status = new_status


@dataclass
class TweetQueue:
    tweets: list[TrackTweet] = field(default_factory=list)

    def __len__(self):
        return len(self.tweets)

    def __iter__(self):
        yield from self.tweets

    @property
    def tweets_not_sent(self):
        return [tweet for tweet in self.tweets if not tweet.sent_status]

    @property
    def tweets_not_generated(self):
        return [tweet for tweet in self.tweets if not tweet.gen_status]
    
    @property
    def tweets_ready_for_sending(self):
        return [tweet for tweet in self.tweets if tweet.gen_status and not tweet.sent_status]

    def enqueue(self, tweet):
        # print(f"{tweet.to_str()} will be added.")
        self.tweets.append(tweet)

    def dequeue(self):
        # print(f"{self.tweets[0].to_str()} will be removed.")
        return self.tweets.popleft()

    @classmethod
    def from_text_file(cls, text_file):
        _tweets = cls()
        for tweet_line in open(text_file, "r"):
            tweet = TrackTweet.from_str(tweet_line)
            _tweets.enqueue(tweet)
        return _tweets

    def to_text_file(self, text_file):
        with open(text_file, "w") as f:
            for tweet in self.tweets:
                tweet_line = tweet.to_str()
                f.write(tweet_line)
