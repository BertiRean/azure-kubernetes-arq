from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, month, avg, when, regexp_replace, expr
from pyspark.sql.functions import col

spark = SparkSession.builder.master("yarn").appName("Arq-App").config(
  map={
    "spark.sql.legacy.timeParserPolicy" : "LEGACY",
    "spark.submit.deployMode" : "client"
  }
).getOrCreate()

#Se lee el archivo

df = spark.read.csv("TGN_Entrega_GBA_Agosto.csv", header="true",sep=";")
df.show(10)

# Volumen Nominal Total por Mes

# Convertir la columna 'fecha' al formato de fecha correcto

df1 = df.withColumn('Fecha',when(expr("substring(Fecha, 5, 1) = '/'"), to_date('Fecha', 'dd/MM/yyyy')).otherwise(to_date('Fecha', 'MM/dd/yyyy')))

# Reemplazar comas en 'volumen nominado' y convertir a tipo numérico

df2 = df1.withColumn('Volumen Nominado (miles m3)',regexp_replace('Volumen Nominado (miles m3)', ',', '').cast('double'))

# Reemplazar nulos en 'volumen nominado' con 0

df2 = df2.withColumn('Volumen Nominado (miles m3)', when(col('Volumen Nominado (miles m3)').isNull(), 0).otherwise(col('Volumen Nominado (miles m3)')))

result = df2.groupBy(month('Fecha').alias('mes')).agg(avg('Volumen Nominado (miles m3)').alias('volumen_nominado_promedio'),sum(col('Volumen Nominado (miles m3)').cast('float')).alias('volumen_nominado_total'))

print("Volumen Nominado Total por mes")
result.show()

# Calcular la sumatoria de volúmenes nominados por Punto de Entrega y Gasoducto

result2 = df2.groupBy('Punto de Entrega','Gasoducto').agg(sum('Volumen Nominado (miles m3)').alias('sumatoria_volumen_nominado'))

print("Volumen Nominado Total: Por Gasoducto y Puntos de Entrega")
result2.show(10)


# Calcular la sumatoria de volúmenes autorizados por Punto de Entrega y Gasoducto

# Reemplazar comas en 'volumen nominado' y convertir a tipo numérico
df3 = df2.withColumn('Volumen Autorizado (miles m3)',regexp_replace('Volumen Autorizado (miles m3)', ',', '').cast('double'))

# Reemplazar nulos en 'volumen nominado' con 0
df3 = df3.withColumn('Volumen Autorizado (miles m3)', when(col('Volumen Autorizado (miles m3)').isNull(), 0).otherwise(col('Volumen Autorizado (miles m3)')))

result3 = df3.groupBy('Punto de Entrega','Gasoducto').agg(sum('Volumen Autorizado (miles m3)').alias('sumatoria_volumen_autorizado'))

print("Volumen Autorizado Total: Por Gasoducto y Puntos de Entrega")
result3.show()

# Calcular la cantidad de entregas por cargador

from pyspark.sql.functions import count

result4 = df3.groupBy('Cargadores').agg(count('Fecha').alias('cantidad_entregas'))

print("Cantidad de Entregas por Cargador")
result4.show()