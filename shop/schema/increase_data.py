import json
import random
from pprint import pprint
import copy

with open('chonggo_schema.json', 'r') as f:
    data = json.load(f)[0]

# print(data)

new_data = []

for j in range(100000):
    tmp_data = copy.deepcopy(data)
    id = int(random.random() * 10000000)
    tmp_data['id'] = id
    new_data.append(tmp_data)

# pprint(new_data[:10])

with open('new_data.json', 'w') as f:
    json.dump(new_data, f)
    
