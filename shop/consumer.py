from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ES_URL = config['DEFAULT']['ES_URL']

def updated_by_query(index, shop_id, delivery_time):
    es = Elasticsearch(ES_URL)
    body = {
            "script": {
                "inline": f"ctx._source.delivery_time = {delivery_time}",
            },
            "query": {
                "term": {
                    "shop_id": {
                        "value": shop_id
                }
            }
        }
    }
    res = es.update_by_query(index=index, body=body)
    print(res)


consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['localhost:9092'],
)
for message in consumer:
    msg = json.loads(message.value.decode('utf-8'))
    shop_id = msg['shop_id']
    delivery_time = msg['delivery_time']
    updated_by_query('shop', shop_id, delivery_time)
