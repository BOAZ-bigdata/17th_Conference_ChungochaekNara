import configparser
import tweepy
import json
from kafka import KafkaProducer

config = configparser.ConfigParser()
config.read('config.ini')

# API_KEY = config['tweeter_auth']['api_key']
# API_SECRET = config['tweeter_auth']['api_secret']
# ACCESS_TOKEN = config['tweeter_auth']['access_token']
# ACCESS_TOKEN_SECRET = config['tweeter_auth']['access_token_secret']
BEARER_TOKEN = config['tweeter_auth']['bearer_token']

class TwitterStream(tweepy.StreamingClient):
    def on_data(self, raw_data):
        json_ = json.loads(raw_data)
        producer.send("twitter_tweet", json_["data"]["text"])
        # print(json_["data"]["text"])
        return True
    def on_error(self, status):
        print(status)

producer = KafkaProducer(acks=1,
                         bootstrap_servers='localhost:9092',
                         value_serializer = lambda v: json.dumps(v).encode("utf-8")
                         )


# CreateStream Client Instance
client = TwitterStream(BEARER_TOKEN)

# Add Stream Rules
client.add_rules(tweepy.StreamRule(value="covid19"))

# Start Stream
client.filter()
