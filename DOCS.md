# Elasticsearch Tutorial

## Introduction
Elasticsearch is a powerful, distributed search engine built on Apache Lucene. It is used for searching, analyzing, and visualizing large volumes of data in real time. This tutorial is designed for beginners who have never worked with Elasticsearch before.

---

## 1. Setting Up Elasticsearch

### 1.1 Installing Elasticsearch

#### **Using Docker (Recommended)**
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.5.0

docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.5.0
```

#### **Manual Installation**
1. Download Elasticsearch from [elastic.co](https://www.elastic.co/downloads/elasticsearch)
2. Extract the downloaded archive.
3. Run Elasticsearch using:
   ```bash
   ./bin/elasticsearch
   ```

4. Verify it is running:
   ```bash
   curl http://localhost:9200
   ```

---

## 2. Understanding Elasticsearch Concepts

- **Index:** A collection of documents (like a database in SQL).
- **Document:** A JSON object representing a single record.
- **Shard:** A division of the index to distribute data across nodes.
- **Replica:** A copy of a shard for fault tolerance.
- **Mapping:** Defines the structure of data in an index.
- **Query DSL:** The language used to search for data.

---

## 3. Basic Elasticsearch Commands

### 3.1 Creating an Index
```bash
curl -X PUT "http://localhost:9200/my_index"
```

### 3.2 Checking Indexes
```bash
curl -X GET "http://localhost:9200/_cat/indices?v"
```

### 3.3 Deleting an Index
```bash
curl -X DELETE "http://localhost:9200/my_index"
```

---

## 4. Working with Documents

### 4.1 Adding a Document
```bash
curl -X POST "http://localhost:9200/my_index/_doc/1" -H 'Content-Type: application/json' -d'
{
  "name": "John Doe",
  "age": 30,
  "city": "New York"
}'
```

### 4.2 Retrieving a Document
```bash
curl -X GET "http://localhost:9200/my_index/_doc/1"
```

### 4.3 Updating a Document
```bash
curl -X POST "http://localhost:9200/my_index/_update/1" -H 'Content-Type: application/json' -d'
{
  "doc": {
    "age": 31
  }
}'
```

### 4.4 Deleting a Document
```bash
curl -X DELETE "http://localhost:9200/my_index/_doc/1"
```

---

## 5. Searching in Elasticsearch

### 5.1 Basic Search
```bash
curl -X GET "http://localhost:9200/my_index/_search?q=name:John"
```

### 5.2 Query DSL Search
```bash
curl -X GET "http://localhost:9200/my_index/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "city": "New York"
    }
  }
}'
```

---

## 6. Advanced Topics

### 6.1 Aggregations
```bash
curl -X GET "http://localhost:9200/my_index/_search" -H 'Content-Type: application/json' -d'
{
  "aggs": {
    "avg_age": {
      "avg": {
        "field": "age"
      }
    }
  }
}'
```

### 6.2 Bulk Indexing
```bash
curl -X POST "http://localhost:9200/my_index/_bulk" -H 'Content-Type: application/json' -d'
{ "index": { "_id": "2" } }
{ "name": "Jane Doe", "age": 28, "city": "Los Angeles" }
{ "index": { "_id": "3" } }
{ "name": "Sam Smith", "age": 35, "city": "Chicago" }
'
```

### 6.3 Deleting an Index
```bash
curl -X DELETE "http://localhost:9200/my_index"
```

---

## 7. Monitoring Elasticsearch

### 7.1 Cluster Health
```bash
curl -X GET "http://localhost:9200/_cluster/health?pretty"
```

### 7.2 Node Stats
```bash
curl -X GET "http://localhost:9200/_nodes/stats"
```

---

## 8. Kibana - Visualizing Elasticsearch Data

Kibana is a web-based interface for visualizing Elasticsearch data.

### 8.1 Running Kibana
```bash
docker run -d --name kibana -p 5601:5601 --link elasticsearch docker.elastic.co/kibana/kibana:8.5.0
```

### 8.2 Access Kibana
Go to: [http://localhost:5601](http://localhost:5601)

### 8.3 Creating Visualizations
1. Open **Kibana Dashboard**.
2. Select **Index Patterns** and add `my_index`.
3. Use **Discover**, **Visualizations**, and **Dashboards** to analyze data.
