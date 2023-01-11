import random
import json
import time
from kafka import KafkaProducer

with open('nested_data.json', 'r') as f:
    nested_data = json.load(f)

class DataUpdator:
    def on_data(self):
        while True:
            n = random.randint(0, 1103)
            update_data = {
                "shop_id": nested_data[n]['shop_id'],
                "delivery_time": random.randint(20, 60)
            }

            time.sleep(random.randint(1, 3))

            producer.send("test", value=update_data)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         key_serializer = None ,

                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))

data_updator = DataUpdator()
data_updator.on_data()
