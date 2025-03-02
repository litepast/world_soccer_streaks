import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


# Create a SparkSession
#spark = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()
sample_data = [{"name": "John    D.", "age": 30},
  {"name": "Alice   G.", "age": 25},
  {"name": "Bob  T.", "age": 35},
  {"name": "Eve   A.", "age": 28}]

st = time.time()

spark = SparkSession.builder \
    .master("local[1]") \
    .appName("FastestSpark") \
    .config("spark.driver.memory", "1g") \
    .config("spark.sql.shuffle.partitions", "1") \
    .config("spark.executor.instances", "1") \
    .config("spark.driver.extraJavaOptions", "-Dio.netty.tryReflectionSetAccessible=true") \
    .config("spark.executor.heartbeatInterval", "60s") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .getOrCreate()

df = spark.read.csv("all_matches.csv", header=True, inferSchema=True)

df.show()









elapsed_time = time.time() - st
print('TL time', elapsed_time, 'seconds')