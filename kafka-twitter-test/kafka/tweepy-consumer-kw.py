from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'twitter_topic',
     bootstrap_servers=['localhost:9092'],
)
for message in consumer:
    msg = json.loads(message.value.decode('utf-8'))
    # print(msg)