# import streamlit as st
# import pandas as pd
# from io import BytesIO
# import databricks.sql

# # Função para consultar o Databricks
# def consultar_databricks(query):
#     with databricks.sql.connect(
#         server_hostname="SEU_HOSTNAME",
#         http_path="SEU_HTTP_PATH",
#         access_token="SEU_TOKEN"
#     ) as connection:
#         with connection.cursor() as cursor:
#             cursor.execute(query)
#             result = cursor.fetchall()
#             columns = [desc[0] for desc in cursor.description]
#             return pd.DataFrame(result, columns=columns)

# st.markdown(
#     "<span style='font-size:22px;color:#A259F7;'>Olá, eu sou a Debora, sua assistente virtual!</span>",
#     unsafe_allow_html=True
# )

# pergunta = st.text_input("Faça aqui a sua busca e encontre a melhor opção :")

# if pergunta:
#     # Exemplo simples: transformar a pergunta em uma query SQL
#     # Aqui você pode usar NLP ou regras para transformar perguntas em queries
#     if "clientes" in pergunta.lower():
#         query = "SELECT * FROM clientes LIMIT 10"
#         df = consultar_databricks(query)
#         st.write(df)
#     else:
#         st.write("Desculpe, ainda não sei responder essa pergunta.")

# # Adicione isso ao final do arquivo
# st.markdown(
#     """
#     <style>
#     .fixed-doll {
#         position: fixed;
#         right: 30px;
#         bottom: 30px;
#         z-index: 9999;
#     }
#     .fixed-doll:hover {
#         transform: scale(1.1);
#         transition: 0.2s;
#         cursor: pointer;
#     }
#     </style>
#     <a href="#" class="fixed-doll">
#         <img src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fnegocios.arrazzei.com%2F2024%2F10%2F10%2F7-melhores-criadores-de-avatar-de-ia-faceis-de-usar%2F%3Fsrsltid%3DAfmBOop6B4ZdQrQHDJQ2c9voUUiNjqGh8We20UdetrNn2a94qbtr8nGH&psig=AOvVaw29VHJdnP_hbk6KHI6jVkh4&ust=1752181107940000&source=images&cd=vfe&opi=89978449&ved=0CBUQjRxqFwoTCNC-j47asI4DFQAAAAAdAAAAABA1" width="120"/>
#     </a>
#     """,
#     unsafe_allow_html=True
# )
# # ...existing code...