from pyspark.sql import SparkSession

# Inicializar a sessão do Spark
spark = SparkSession.builder \
    .appName("Spark Job com PostgreSQL") \
    .getOrCreate()

# Configurações de conexão com o PostgreSQL
jdbc_url = "jdbc:postgresql://postgresql-service:5432/postgres"
propriedades = {
    "user": "postgres",
    "password": "nJLE2y4i7j",
    "driver": "org.postgresql.Driver"
}

# Ler dados da tabela 'itens_pedido' do PostgreSQL
df = spark.read.jdbc(url=jdbc_url, table="itens_pedido", properties=propriedades)

# Exibir esquema da tabela
df.printSchema()

# Mostrar os primeiros registros
df.show()

# Exemplo de transformação simples: agregação por região (modificar conforme a tabela real)
df_aggregated = df.groupBy("codigo").sum("qtd_solicitada")

# Exibir o resultado da agregação
df_aggregated.show()

# Salvar os dados agregados de volta no PostgreSQL (sobrescrevendo a tabela existente)
df_aggregated.write.jdbc(url=jdbc_url, table="itens_pedido_aggregated", mode="overwrite", properties=propriedades)

# Ou salvar os dados em formato Parquet em um diretório
df_aggregated.write.parquet("/mnt/spark_output/itens_pedido_aggregated")

# Fechar a sessão do Spark
spark.stop()
