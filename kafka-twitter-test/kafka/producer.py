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
        if json_["data"]["lang"] == "ko":
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

# Delete Rules Function, If there are no rules, return None
def delete_all_rules(rules):
    if rules is None or rules.data is None:
        return None
    stream_rules = rules.data
    ids = list(map(lambda rule: rule.id, stream_rules))
    client.delete_rules(ids=ids)

# Get All Rules If id is not specified
rules = client.get_rules()

# Delete All Rules
delete_all_rules(rules)

# Add Stream Rules
client.add_rules(tweepy.StreamRule(value="정국"))
print(client.get_rules())

# Start Stream
client.filter(tweet_fields=["lang"])
