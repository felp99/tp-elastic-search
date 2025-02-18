import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

ES_HOST = "http://localhost:9200"
ES_INDEX = "crimedata"

es = Elasticsearch([ES_HOST])

def create_index():
    if not es.indices.exists(index=ES_INDEX):
        es.indices.create(index=ES_INDEX)

def load_csv_to_elasticsearch(csv_file):
    df = pd.read_csv(csv_file)
    df.fillna("", inplace=True)

    actions = [
        {
            "_index": ES_INDEX,
            "_id": row["DR_NO"],
            "_source": row.to_dict()
        }
        for _, row in df.iterrows()
    ]

    success, _ = bulk(es, actions)
    print(f"Inserted {success} records into Elasticsearch")

if __name__ == "__main__":
    create_index()
    load_csv_to_elasticsearch("Crime_Data.csv")
