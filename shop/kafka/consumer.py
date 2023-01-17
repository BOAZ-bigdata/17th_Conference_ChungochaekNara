from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import configparser
from es_updator import upsert_bulk_to_index

with open('../schema/split_data.json', 'r') as f:
    nested_data = json.load(f)

config = configparser.ConfigParser()
config.read('config.ini')

ES_URL = "http://localhost:9200"

def updated_by_query(index, id, customerReviewRank):
    es = Elasticsearch(ES_URL)
    body = {
            "script": {
                "inline": f"ctx._source.customerReviewRank = {customerReviewRank}",
            },
            "query": {
                "term": {
                    "id": {
                        "value": id
                }
            }
        }
    }
    res = es.update_by_query(index=index, body=body)
    print(res)


consumer = KafkaConsumer(
    'test1',
     bootstrap_servers=['localhost:9092'],
)

data = []

for message in consumer:
    msg = json.loads(message.value.decode('utf-8'))
    data.append(msg)
    if len(data) >= 1000:
        upsert_bulk_to_index('book_split', data)
        data.clear()

