import streamlit as st
import pandas as pd
from io import BytesIO
import databricks.sql

# Função para consultar o Databricks
def consultar_databricks(query):
    with databricks.sql.connect(
        server_hostname="SEU_HOSTNAME",
        http_path="SEU_HTTP_PATH",
        access_token="SEU_TOKEN"
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)

st.title("Agente de Perguntas com Databricks")

pergunta = st.text_input("Faça sua pergunta:")

if pergunta:
    # Exemplo simples: transformar a pergunta em uma query SQL
    # Aqui você pode usar NLP ou regras para transformar perguntas em queries
    if "clientes" in pergunta.lower():
        query = "SELECT * FROM clientes LIMIT 10"
        df = consultar_databricks(query)
        st.write(df)
    else:
        st.write("Desculpe, ainda não sei responder essa pergunta.")