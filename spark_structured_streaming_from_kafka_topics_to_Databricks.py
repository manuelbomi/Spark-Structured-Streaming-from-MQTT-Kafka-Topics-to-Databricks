df = (spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "<your_kafka_bootstrap_servers>")
  .option("subscribe", "<your_kafka_topic>")
  .option("startingOffsets", "latest") # or "earliest" for initial load
  .load())

# Further processing (e.g., parsing JSON, transformations, aggregations)
# Example: Assuming data is JSON in the 'value' column
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType

schema = StructType() \
    .add("device_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("temperature", DoubleType())

processed_df = df.selectExpr("CAST(value AS STRING) as json_data") \
    .withColumn("data", from_json(col("json_data"), schema)) \
    .select("data.*")

# Write to Delta Lake (or other sink)
(processed_df.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", "/mnt/delta/checkpoints/<your_checkpoint_path>")
  .trigger(processingTime="1 minute") # or availableNow=True for incremental batch
  .toTable("<your_delta_table_name>"))