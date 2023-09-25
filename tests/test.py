from pyspark.sql import SparkSession

host = "spark://127.0.0.1:62455"

spark = SparkSession.builder.master(host).appName("My App").config(
  "spark.submit.deployMode", "client"
).getOrCreate()

if spark.getActiveSession():
  df = spark.read.csv("TGN_Entrega_GBA_Agosto.csv", header="true",sep=";")
  df.show(10)


