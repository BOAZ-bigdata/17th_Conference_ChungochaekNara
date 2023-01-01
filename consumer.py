from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'twitter_topic',
     bootstrap_server=['localhost:9092'],
     value_serializer = lambda v: json.dumps(v).encode("utf-8")
)

for message in consumer:
    msg = json.loads(message.value)
    