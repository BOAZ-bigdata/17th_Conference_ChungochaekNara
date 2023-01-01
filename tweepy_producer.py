import configparser
import tweepy
import json
from kafka import KafkaProducer

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['tweeter_auth']['api_key']
API_SECRET = config['tweeter_auth']['api_secret']
ACCESS_TOKEN = config['tweeter_auth']['access_token']
ACCESS_TOKEN_SECRET = config['tweeter_auth']['access_token_secret']
BEARER_TOKEN = config['tweeter_auth']['bearer_token']

class TwitterStream(tweepy.StreamingClient):
    def on_data(self, raw_data):
        json_ = json.loads(raw_data)
        producer.send("test", value=json_['text'].encode('utf-8'))
        return True
    def on_error(self, status):
        print(status)

producer = KafkaProducer(acks=0, 
                         bootstrap_server=['localhost:9092'],
                         value_serializer = lambda v: json.dumps(v).encode("utf-8")
                    )

# 스트림 클라이언트 인스턴스 생성
client = TwitterStream(BEARER_TOKEN)

# 스트림 규칙 추가
client.add_rules(tweepy.StreamRule(value=""))

# 스트림 시작
client.filter()
