import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st

df_candidatos = pd.read_csv('pages/candidatos_final.csv', on_bad_lines='skip', sep=';') 
df_vagas = pd.read_csv('pages/vagas_final.csv', on_bad_lines='skip', sep=';')

# Exibição lúdica das colunas
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🧑‍💼 Info Candidatos")
    st.code('\n'.join(df_candidatos.columns.tolist()), language='python')
with col2:
    st.markdown("### 💼 Info Vagas")
    st.code('\n'.join(df_vagas.columns.tolist()), language='python')

# Criar texto consolidado do candidato
df_candidatos['perfil_texto'] = (
    df_candidatos['objetivo_profissional'].fillna('') + ' ' +
    df_candidatos['titulo_profissional'].fillna('') + ' ' +
    df_candidatos['nivel_profissional'].fillna('') + ' ' +
    df_candidatos['nivel_academico'].fillna('') + ' ' +
    df_candidatos['nivel_ingles'].fillna('') + ' ' +
    df_candidatos['nivel_espanhol'].fillna('') + ' ' +
    df_candidatos['outro_idioma'].fillna('') + ' ' +
    df_candidatos['cursos'].fillna('') + ' ' +
    df_candidatos['atuacao'].fillna('')
)

# Criar texto consolidado da vaga
df_vagas['texto_vaga'] = (
    df_vagas['titulo_padronizado'].fillna('') + ' ' +
    df_vagas['atuacao_tokenizadas'].fillna('') + ' ' +
    df_vagas['atividade_tokenizadas'].fillna('') + ' ' +
    df_vagas['competencias_tokenizadas'].fillna('')
)

# Função de ranqueamento
def ranquear_candidatos(vaga_texto, candidatos_textos, top_n=5):
    corpus = [vaga_texto] + candidatos_textos
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    top_indices = cosine_sim.argsort()[::-1][:top_n]
    return top_indices, cosine_sim[top_indices]

# Escolher uma vaga pelo título original
titulo_vaga_escolhida = "Desenvolvedor SAP SD - 713"  # substitua pelo título desejado

# Filtrar a vaga pelo título original
vaga_filtrada = df_vagas[df_vagas['titulo_original'] == titulo_vaga_escolhida]
if vaga_filtrada.empty:
    st.error("Vaga não encontrada!")
    st.stop()
vaga = vaga_filtrada.iloc[0]
texto_vaga = vaga['texto_vaga']
id_vaga_escolhida = vaga['id_todos_digitos']  # pega o id correto da vaga filtrada

# Obter top 5 candidatos
indices, scores = ranquear_candidatos(texto_vaga, df_candidatos['perfil_texto'].tolist())
top_candidatos = df_candidatos.iloc[indices].copy()
top_candidatos['score_aderencia'] = scores

# Mostrar resultado no Streamlit
colunas_necessarias = ['codigo_profissional', 'nome', 'perfil_texto', 'score_aderencia']
for coluna in colunas_necessarias:
    if coluna not in top_candidatos.columns:
        st.warning(f"Coluna '{coluna}' não encontrada em df_candidatos.")

st.subheader(f'Top 5 Candidatos para a Vaga {id_vaga_escolhida}')
st.dataframe(top_candidatos[colunas_necessarias])

# Criar o gráfico de barras horizontais
plt.figure(figsize=(10, 6))
sns.barplot(
    x='score_aderencia',
    y='nome',
    data=top_candidatos.sort_values(by='score_aderencia', ascending=False),
    palette='viridis'
)
plt.title(f'Top 5 Candidatos para a Vaga {id_vaga_escolhida} por Score de Aderência')
plt.xlabel('Score de Aderência')
plt.ylabel('Nome do Candidato')
plt.xlim(0, 1)
plt.tight_layout()

# Exibir gráfico no Streamlit
st.pyplot(plt)