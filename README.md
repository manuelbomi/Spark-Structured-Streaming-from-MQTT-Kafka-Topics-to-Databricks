# Spark Structured Streaming from MQTT Kafka Topics to Databricks


### 1. IoT Devices to Kafka:

- MQTT Broker: IoT devices typically send data via MQTT to an MQTT broker.

- MQTT to Kafka Bridge: A component or service is needed to bridge the data from the MQTT broker to Kafka. This can be a custom application, a dedicated connector (like Confluent MQTT Source Connector), or a platform like HIQ Edge and Data Hub. This component subscribes to MQTT topics and publishes the messages to corresponding Kafka topics.

### 2. Kafka to Databricks:

- Spark Structured Streaming: Databricks uses Spark Structured Streaming to read data continuously from Kafka topics.

- Kafka Connector: The built-in Kafka connector in Spark is used to establish the connection and subscribe to the desired Kafka topics.

## Key Steps for Ingesting Data from Kafka into Databricks

* Configure Kafka Connection Details.
  
* You need to provide the Kafka bootstrap servers and the topic(s) you wish to subscribe to. If using SSL or other security protocols, these configurations also need to be specified.


```ruby
    kafka_bootstrap_servers = "your_kafka_broker_1:9092,your_kafka_broker_2:9092"
    kafka_topic = "your_kafka_topic_name"
```
---

* Read from Kafka using Structured Streaming.
  
#### Databricks' Structured Streaming allows you to treat Kafka topics as streaming sources. You can use the readStream method to subscribe to a topic.


```ruby
    df = spark.readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
      .option("subscribe", kafka_topic) \
      .option("startingOffsets", "earliest") \
      .load()

```

- format("kafka"): Specifies Kafka as the data source.
  
- option("kafka.bootstrap.servers", ...): Sets the Kafka broker addresses.
  
- option("subscribe", ...): Defines the Kafka topic(s) to read from.
  
- option("startingOffsets", "earliest"): Configures the starting point for reading data (e.g., from the beginning of the topic).

---

## Process and Transform Data 

#### Once the data is ingested into a DataFrame, you can perform various transformations, deserialization, and schema adjustments as needed. Kafka messages typically arrive with key, value, topic, partition, and offset columns. You'll likely need to deserialize the value column, which is often in a format like JSON or Avro.


```ruby
    from pyspark.sql.functions import col, from_json
    from pyspark.sql.types import StructType, StringType, IntegerType

    # Example schema for JSON deserialization
    schema = StructType([
        StringType().alias("id"),
        StringType().alias("name"),
        IntegerType().alias("age")
    ])

    processed_df = df.selectExpr("CAST(value AS STRING) as json_value") \
      .withColumn("data", from_json(col("json_value"), schema)) \
      .select("data.*")

```
---

## Write Data to a Destination.

#### After processing, you can write the data to a desired destination within Databricks, such as a Delta Lake table for persistent storage and further analysis.

```ruby
    checkpoint_location = "/path/to/checkpoint/location" # Required for Structured Streaming
    output_table_name = "your_delta_table_name"
    processed_df.writeStream \
      .format("delta") \
      .outputMode("append") \
      .option("checkpointLocation", checkpoint_location) \
      .toTable(output_table_name)
```

- format("delta"): Specifies Delta Lake as the sink.
  
- outputMode("append"): Configures how new data is written to the table.
  
- option("checkpointLocation", ...): Essential for fault tolerance in Structured Streaming.

---

## Using Streaming Tables with Databricks SQL

For a more declarative approach in Databricks SQL, especially with Unity Catalog, you can use streaming tables to ingest data incrementally from Kafka.

```ruby
CREATE OR REFRESH STREAMING TABLE your_streaming_table
AS SELECT * FROM kafka.read_kafka(
  bootstrapServers => 'your_kafka_broker_1:9092',
  subscribe => 'your_kafka_topic_name'
);
```

---


Thank you for reading


### **AUTHOR'S BACKGROUND**
### Author's Name:  Emmanuel Oyekanlu
```
Skillset:   I have experience spanning several years in data science, developing scalable enterprise data pipelines,
enterprise solution architecture, architecting enterprise systems data and AI applications,
software and AI solution design and deployments, data engineering, IoT & RFID applications,  high performance computing (GPU, CUDA), machine learning,
NLP, Agentic-AI and LLM applications as well as deploying scalable solutions (apps) on-prem and in the cloud.

I can be reached through: manuelbomi@yahoo.com

Website:  http://emmanueloyekanlu.com/
Publications:  https://scholar.google.com/citations?user=S-jTMfkAAAAJ&hl=en
LinkedIn:  https://www.linkedin.com/in/emmanuel-oyekanlu-6ba98616
Github:  https://github.com/manuelbomi

```
[![Icons](https://skillicons.dev/icons?i=aws,azure,gcp,scala,mongodb,redis,cassandra,kafka,anaconda,matlab,nodejs,django,py,c,anaconda,git,github,mysql,docker,kubernetes&theme=dark)](https://skillicons.dev)






