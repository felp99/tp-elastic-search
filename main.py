import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

ES_HOST = "http://localhost:9200"
ES_INDEX = "kepler_data"

# Initialize Elasticsearch client
es = Elasticsearch([ES_HOST])

def create_index():
    """Creates an index with mapping if it doesn't exist."""
    if not es.indices.exists(index=ES_INDEX):
        mappings = {
            "mappings": {
                "properties": {
                    "rowid": {"type": "integer"},
                    "kepid": {"type": "integer"},
                    "kepoi_name": {"type": "keyword"},
                    "kepler_name": {"type": "keyword"},
                    "koi_disposition": {"type": "keyword"},
                    "koi_pdisposition": {"type": "keyword"},
                    "koi_score": {"type": "float"},
                    "koi_period": {"type": "float"},
                    "koi_time0bk": {"type": "float"},
                    "koi_impact": {"type": "float"},
                    "koi_duration": {"type": "float"},
                    "koi_depth": {"type": "float"},
                    "koi_prad": {"type": "float"},
                    "koi_teq": {"type": "float"},
                    "koi_insol": {"type": "float"},
                    "koi_model_snr": {"type": "float"},
                    "koi_tce_plnt_num": {"type": "integer"},
                    "ra": {"type": "float"},
                    "dec": {"type": "float"},
                    "koi_kepmag": {"type": "float"}
                }
            }
        }
        es.indices.create(index=ES_INDEX, body=mappings)
        print(f"Index '{ES_INDEX}' created successfully.")
    else:
        print(f"Index '{ES_INDEX}' already exists.")

def load_csv_to_elasticsearch(csv_file):
    """Reads a CSV file and inserts records into Elasticsearch."""
    df = pd.read_csv(csv_file)
    df.fillna("", inplace=True)

    actions = [
        {
            "_index": ES_INDEX,
            "_id": row["rowid"],
            "_source": row.to_dict()
        }
        for _, row in df.iterrows()
    ]

    success, _ = bulk(es, actions)
    print(f"Inserted {success} records into Elasticsearch")

if __name__ == "__main__":
    create_index()
    load_csv_to_elasticsearch("cumulative.csv")
