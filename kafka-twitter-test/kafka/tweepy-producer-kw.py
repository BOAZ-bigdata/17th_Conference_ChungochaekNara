from __future__ import absolute_import

from datetime import datetime
import threading, time
import configparser

from kafka import KafkaProducer

import tweepy

from tweepy import OAuthHandler, StreamingClient
from tweepy import Stream, StreamRule

import json

config = configparser.ConfigParser()
config.read('config.ini')

"""API ACCESS KEYS"""
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOoJjwEAAAAAv3PKcI3y5Ydn2YfEa2xzerXcVLQ%3DjkxLCPi0Wg5Vp6566FS9s6hf66VyjcBOuTltaKfWU25UQ5hUpu"

class TwitterStream(tweepy.StreamingClient):
    def on_data(self, raw_data):
        json_ = json.loads(raw_data)
        producer.send("twitter_topic", value=json_['data']['text'])
        return True
    def on_error(self, status):
        print(status)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         key_serializer = None ,
                         
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))

# 스트림 클라이언트 인스턴스 생성
client = TwitterStream(BEARER_TOKEN)

# 스트림 규칙 추가
client.add_rules(tweepy.StreamRule(value="covid19"))
# client.add_rules(tweepy.StreamRule(lang="ko"))

# 스트림 시작
client.filter()