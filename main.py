import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

ES_HOST = "http://localhost:9200"
ES_INDEX = "crimedata"

# Initialize Elasticsearch client
es = Elasticsearch([ES_HOST])

def create_index():
    """Creates an index with mapping if it doesn't exist."""
    if not es.indices.exists(index=ES_INDEX):
        mappings = {
            "mappings": {
                "properties": {
                    "DR_NO": {"type": "keyword"},  # Changed 'rowid' to 'DR_NO' for document ID
                    "Date Rptd": {"type": "date"},
                    "DATE OCC": {"type": "date"},
                    "TIME OCC": {"type": "keyword"},
                    "AREA": {"type": "keyword"},
                    "AREA NAME": {"type": "keyword"},
                    "Rpt Dist No": {"type": "keyword"},
                    "Part 1-2": {"type": "keyword"},
                    "Crm Cd": {"type": "keyword"},
                    "Crm Cd Desc": {"type": "keyword"},
                    "Mocodes": {"type": "keyword"},
                    "Vict Age": {"type": "integer"},
                    "Vict Sex": {"type": "keyword"},
                    "Vict Descent": {"type": "keyword"},
                    "Premis Cd": {"type": "keyword"},
                    "Premis Desc": {"type": "keyword"},
                    "Weapon Used Cd": {"type": "keyword"},
                    "Weapon Desc": {"type": "keyword"},
                    "Status": {"type": "keyword"},
                    "Status Desc": {"type": "keyword"},
                    "LOCATION": {"type": "geo_point"},  # Assuming 'LOCATION' is geospatial
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
    print("Columns in CSV:", df.columns)

    df.fillna("", inplace=True)  # Handle missing values

    # Convert DataFrame rows to JSON and insert into Elasticsearch
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
    load_csv_to_elasticsearch("Crime_Data.csv")
