from pyspark.sql import SparkSession
import pyspark.sql.functions as sf
from sklearn.svm import SVC

from train import train_data
from functools import partial
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ =='__main__':
    model=SVC()

    spark = SparkSession.builder \
    .appName("Lab_04") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

    df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "train-data") \
    .option("startingOffsets", "earliest") \
    .load()

    wrapped_fn = partial(
        train_data,model=model
    )

    query=df.selectExpr("CAST(value AS STRING) as value")\
        .select(sf.from_json(sf.col('value'),'data binary, label INT').alias('parse'))\
        .select('parse.data','parse.label')\
        .writeStream\
        .foreachBatch(wrapped_fn) \
        .start()
    query.awaitTermination()

