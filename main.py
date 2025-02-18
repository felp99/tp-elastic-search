import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

# Elasticsearch Configuration
ES_HOST = "http://localhost:9200"  # Change to your Elasticsearch instance URL
ES_INDEX = "crime_data"

# Initialize Elasticsearch client
es = Elasticsearch([ES_HOST])

def create_index():
    """Creates an index with mapping if it doesn't exist."""
    if not es.indices.exists(index=ES_INDEX):
        mappings = {
            "mappings": {
                "properties": {
                    "DR_NO": {"type": "keyword"},
                    "Date Rptd": {"type": "date", "format": "MM/dd/yyyy HH:mm:ss a"},
                    "DATE OCC": {"type": "date", "format": "MM/dd/yyyy HH:mm:ss a"},
                    "TIME OCC": {"type": "integer"},
                    "AREA": {"type": "keyword"},
                    "AREA NAME": {"type": "keyword"},
                    "Rpt Dist No": {"type": "integer"},
                    "Part 1-2": {"type": "integer"},
                    "Crm Cd": {"type": "integer"},
                    "Crm Cd Desc": {"type": "text"},
                    "Vict Age": {"type": "integer"},
                    "Vict Sex": {"type": "keyword"},
                    "Vict Descent": {"type": "keyword"},
                    "Premis Cd": {"type": "integer"},
                    "Premis Desc": {"type": "text"},
                    "Weapon Used Cd": {"type": "integer"},
                    "Weapon Desc": {"type": "text"},
                    "Status": {"type": "keyword"},
                    "Status Desc": {"type": "text"},
                    "Crm Cd 1": {"type": "integer"},
                    "Crm Cd 2": {"type": "integer"},
                    "Crm Cd 3": {"type": "integer"},
                    "Crm Cd 4": {"type": "integer"},
                    "LOCATION": {"type": "geo_point"},
                    "Cross Street": {"type": "keyword"},
                    "LAT": {"type": "float"},
                    "LON": {"type": "float"}
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
    df.fillna("", inplace=True)  # Replace NaN values with empty strings

    # Convert DataFrame rows to JSON and insert into Elasticsearch
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
    load_csv_to_elasticsearch("crime_data.csv")  # Replace with your CSV file