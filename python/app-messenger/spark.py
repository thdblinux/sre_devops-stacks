from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Simple Test") \
    .getOrCreate()

print("Spark Session created successfully.")
