import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

df_candidatos = pd.read_csv('candidatos_final.csv')  
df_vagas = pd.read_csv('vagas_final.csv')

print(df_candidatos.columns)
print(df_vagas.columns)

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
    print("Vaga não encontrada!")
    exit()
vaga = vaga_filtrada.iloc[0]
texto_vaga = vaga['texto_vaga']
id_vaga_escolhida = vaga['id_todos_digitos']  # pega o id correto da vaga filtrada

# Obter top 5 candidatos
indices, scores = ranquear_candidatos(texto_vaga, df_candidatos['perfil_texto'].tolist())
top_candidatos = df_candidatos.iloc[indices].copy()
top_candidatos['score_aderencia'] = scores

# Mostrar resultado
colunas_necessarias = ['codigo_profissional', 'nome', 'perfil_texto', 'score_aderencia']
for coluna in colunas_necessarias:
    if coluna not in top_candidatos.columns:
        print(f"Coluna '{coluna}' não encontrada em df_candidatos.")
print(top_candidatos[colunas_necessarias])

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