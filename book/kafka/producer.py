import random
import json
import time
from kafka import KafkaProducer

with open('../data/split_data.json', 'r') as f:
    nested_data = json.load(f)

ids = [i['id'] for i in nested_data]

class DataUpdator:
    def on_data(self):
        while True:
            n = random.choice(ids)
            # update_data = {
            #     "id": n,
            #     "customerReviewRank": random.randint(1, 100000)
            # }
            i = random.randint(0, 90000)
            update_data = nested_data[i]
            update_data['customerReviewRank'] = random.randint(1, 10000)
            
            # time.sleep(random.randint(1, 3))

            producer.send("test1", value=update_data)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         key_serializer = None ,

                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))

data_updator = DataUpdator()
data_updator.on_data()
