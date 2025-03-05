import os
import json 
import time 
from typing import List 
from tqdm import tqdm
from elasticsearch import Elasticsearch
from pprint import pprint

INDEX_NAME = os.getenv("INDEX_NAME", "apod")

def index_data(documents: List[dict]): 
    es = get_es_client(max_retries=50, sleep_time=5)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents)
    pprint(f'Indexed {len(documents)} documents into Elasticsearch index "{INDEX_NAME}"')

def _create_index(es: Elasticsearch) -> dict:
    es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    return es.indices.create(index=INDEX_NAME)

def _insert_documents(es: Elasticsearch, documents: List[dict]) -> dict:
    operations = []
    for document in tqdm(documents, total=len(documents), desc='Indexing documents'):
        operations.append({'index': {'_index': INDEX_NAME}})
        operations.append(document)
    return es.bulk(operations=operations)

def get_es_client(max_retries: int = 5, sleep_time: int = 5) -> Elasticsearch: 
    i = 0
    while i < max_retries: 
        try: 
            es = Elasticsearch('http://elasticsearch:9200')
            client_info = es.info()
            pprint("Connected to Elasticsearch!")
            pprint(f"Cluster info: \n{client_info}")
            return es 
        except Exception as e: 
            print(e)
            pprint("Could not connect to Elasticsearch, retrying...")
            time.sleep(sleep_time)
            i += 1
    raise ConnectionError("Fialed to connect to Elasticsearch after multiple attempts.")

if __name__ == '__main__':
    with open("./data/apod.json") as f: 
        documents = json.load(f)
    index_data(documents)