import configparser
import tweepy
import json
from kafka import KafkaProducer

config = configparser.ConfigParser()
config.read('config.ini')

BEARER_TOKEN = config['tweeter_auth']['bearer_token']

class TwitterStream(tweepy.StreamingClient):
    def on_data(self, raw_data):
        json_ = json.loads(raw_data)
        producer.send("twitter_tweet", json_["data"]["text"])
        #print(json_["data"]["text"])
        return True
    def on_error(self, status):
        print(status)

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                        key_serializer = None,
                         value_serializer = lambda v: json.dumps(v).encode("utf-8")
                         )


# CreateStream Client Instance
client = TwitterStream(BEARER_TOKEN)

# Add Stream Rules
client.add_rules(tweepy.StreamRule(value="covid19"))

# Start Stream
client.filter()

