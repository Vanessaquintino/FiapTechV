import streamlit as st
import pandas as pd
from io import BytesIO
# from databricks import sql

st.set_page_config(page_title="Entrevista de Engajamento", layout="wide")

st.title("📋 Entrevista de Engajamento Profissional")

# Dados do candidato
nome = st.text_input("Nome do candidato")
email = st.text_input("E-mail do candidato")
cargo = st.text_input("Cargo da vaga")

st.markdown("---")

# Estrutura de perguntas por bloco
perguntas = {
    "Propósito e Motivação Pessoal": [
        "O que mais te motiva no seu trabalho atualmente?",
        "Conte sobre um momento em que você se sentiu muito realizado profissionalmente.",
        "O que te atraiu nessa vaga e na nossa empresa?"
    ],
    "Proatividade e Entrega de Valor": [
        "Cite uma iniciativa que você tomou por conta própria para melhorar um processo.",
        "Como você mede seu impacto no trabalho?"
    ],
    "Aprendizado e Evolução Contínua": [
        "Qual foi a última coisa nova que você aprendeu por vontade própria?",
        "Como você lida com feedbacks? Dê um exemplo."
    ],
    "Cultura e Relacionamentos": [
        "Você já trabalhou em um lugar onde se sentia realmente pertencente? Por quê?",
        "Como você contribui para o clima e o engajamento do time?"
    ],
    "Comprometimento e Visão de Futuro": [
        "Como seria sua carreira ideal nos próximos 3 anos?",
        "O que faria você se desligar de uma empresa?"
    ]
}

respostas = {}
notas = {}

# Critérios automáticos: quanto maior a resposta, maior a nota (de 1 a 5)
def calcular_nota(resposta):
    tamanho = len(resposta.strip())
    if tamanho == 0:
        return 1
    elif tamanho < 50:
        return 2
    elif tamanho < 150:
        return 3
    elif tamanho < 300:
        return 4
    else:
        return 5

# Coleta de respostas e notas
for bloco, questoes in perguntas.items():
    st.subheader(f"🧩 {bloco}")
    for i, pergunta in enumerate(questoes):
        resposta = st.text_area(f"📌 {pergunta}", key=f"resp_{bloco}{i}")
        if resposta.strip():
            nota = calcular_nota(resposta)
        else:
            nota = 0
        st.caption(f"Nota automática: {nota} / 5")  # Exibe a nota menor e abaixo
        respostas[pergunta] = resposta
        notas[pergunta] = nota
    st.markdown("---")

# Cálculo da média final
media_engajamento = sum(notas.values()) / len(notas) if notas else 0
st.metric("💡 Engajamento médio do candidato", f"{media_engajamento:.2f} / 5")


#Salvar resultados
if st.button("Salvar Respostas"):
    # Verificação dos campos obrigatórios
    campos_vazios = []
    if not nome.strip():
        campos_vazios.append("Nome do candidato")
    if not email.strip():
        campos_vazios.append("E-mail do candidato")
    if not cargo.strip():
        campos_vazios.append("Cargo da vaga")
    for pergunta, resposta in respostas.items():
        if not resposta.strip():
            campos_vazios.append(f"Resposta: {pergunta}")

    if campos_vazios:
        st.error("Por favor, preencha todos os campos obrigatórios antes de salvar.\n\nCampos faltando:\n- " + "\n- ".join(campos_vazios))
    else:
        df = pd.DataFrame({
            "Pergunta": list(respostas.keys()),
            "Resposta": list(respostas.values()),
            "Nota": list(notas.values())
        })
        df["Candidato"] = nome
        df["Email"] = email
        df["Cargo"] = cargo
        df["Média Engajamento"] = media_engajamento

        # Salvar CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Baixar respostas como CSV", data=csv, file_name=f"{nome}_entrevista.csv", mime="text/csv")

        # Salvar Excel
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Entrevista')
        st.download_button(
            "📥 Baixar respostas como Excel (.xlsx)",
            data=excel_buffer.getvalue(),
            file_name=f"{nome}_entrevista.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.success("Respostas salvas com sucesso!")
# ...existing code...

# ...existing code...

from databricks import sql

# def enviar_para_databricks(df):
#     # Substitua pelos seus dados do Databricks
#     DATABRICKS_SERVER_HOSTNAME = "seu-workspace.cloud.databricks.com"
#     DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/xxxxxxx"
#     DATABRICKS_ACCESS_TOKEN = "dapiXXXXXXXXXXXXXXXXXXXXXXXX"

#     # Conectando ao Databricks
#     with sql.connect(
#         server_hostname=DATABRICKS_SERVER_HOSTNAME,
#         http_path=DATABRICKS_HTTP_PATH,
#         access_token=DATABRICKS_ACCESS_TOKEN
#     ) as connection:
#         cursor = connection.cursor()
#         # Crie a tabela se não existir
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS entrevista_engajamento (
#                 Pergunta STRING,
#                 Resposta STRING,
#                 Nota INT,
#                 Candidato STRING,
#                 Email STRING,
#                 Cargo STRING,
#                 Media_Engajamento DOUBLE
#             )
#         """)
#         # Inserindo os dados linha a linha
#         for _, row in df.iterrows():
#             cursor.execute("""
#                 INSERT INTO entrevista_engajamento (Pergunta, Resposta, Nota, Candidato, Email, Cargo, Media_Engajamento)
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 row["Pergunta"],
#                 row["Resposta"],
#                 int(row["Nota"]),
#                 row["Candidato"],
#                 row["Email"],
#                 row["Cargo"],
#                 float(row["Média Engajamento"])
#             ))
#         cursor.close()

# # ...dentro do bloco else, após salvar o Excel:
#         try:
#             enviar_para_databricks(df)
#             st.success("Respostas salvas e enviadas para o Databricks com sucesso!")
#         except Exception as e:
#             st.error(f"Erro ao enviar para o Databricks: {e}")

# ...existing code...