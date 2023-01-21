import time, json
from typing import List, Dict
import configparser
from pprint import pprint
from elasticsearch import Elasticsearch

config = configparser.ConfigParser()
config.read('../kafka/config.ini')

UPSERT_DELAY_INTERVAL_SECOND = int(config['DEFAULT']['UPSERT_DELAY_INTERVAL_SECOND'])
UPSERT_BATCH_SIZE = int(config['DEFAULT']['UPSERT_BATCH_SIZE'])
USER_FIND_INTERVAL_SECOND = int(config['DEFAULT']['USER_FIND_INTERVAL_SECOND'])
ES_URL = config['DEFAULT']['ES_URL']

def upsert_bulk_to_es(data: List[dict], index_name:str, upsert_delay_interval: int, upsert_batch_size: int):
    from elasticsearch import helpers

    es = Elasticsearch(ES_URL)
    try:
        total = 0
        result = list()
        for doc in data:
            temp = dict()
            temp["_index"] = index_name
            temp["_id"] = doc["id"]

            temp["_source"] = doc
            result.append(temp)
            if len(result) == upsert_batch_size:
                helpers.bulk(es, result)
                total += len(result)
                result = []
                print(f"> {total}/{len(data)} docs inserted")
                time.sleep(upsert_delay_interval)

        if len(result) > 0:
            helpers.bulk(es, result)
            total += len(result)

    except Exception as e:
        print("[Error] Updating post-index failed!")
        print(str(e))
        raise e
    finally:
        if total == len(data):
            print(f"\n >>> Successfully {total} docs has been updated! <<<\n")
        else:
            print(f"\n >>> Only {total} out of {len(data)} docs has been updated! <<<\n")
        es.close()

def upsert_bulk_to_index(index, updated_data):

    if len(updated_data) > 0:

        print("============ Upsert Query Data Preview (First 10 docs)================")
        pprint(updated_data[:10])

        print("======================================================================")
        print(f"Start upserting to ES... total {len(updated_data)} docs")
        t_start = time.time()
        upsert_bulk_to_es(updated_data, index, UPSERT_DELAY_INTERVAL_SECOND, UPSERT_BATCH_SIZE)
        t_end = time.time()
        print("Finish upserting to ES, time elapsed:", t_end-t_start, "seconds")
    else:
        print("\n >>> No data to upsert to ES! <<<\n")
        print("Bye!")

if __name__ == "__main__":
    index_name = "book_split" # 인덱스명

    with open('../data/split_data.json', 'r') as f:
        updated_data = json.load(f)

    upsert_bulk_to_index(index_name, updated_data)
    print("Finish shop index update")

