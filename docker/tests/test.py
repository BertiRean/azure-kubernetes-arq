from doctest import master
from pyspark.sql import SparkSession

host = "spark://20.226.229.151:7077"

spark = SparkSession.builder.master(host).appName("My App").config(
  "spark.submit.deployMode", "client"
).getOrCreate()

df = spark.read.csv("TGN_Entrega_GBA_Agosto.csv", header="true",sep=";")
df.show(10)
