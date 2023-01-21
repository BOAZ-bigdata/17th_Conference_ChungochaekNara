import json

with open('new_data.json', 'r') as f:
    data = json.load(f)

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

split_data = []

for i in range(100000):
    invalid = {"subInfo"}
    split_data.append(without_keys(data[i], invalid))

with open('split_data.json', 'w') as f:
    json.dump(split_data, f)
