import pandas as pd
import nltk
import re
import string0
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import pandas as pd



df_vagas = pd.read_json('vagas.json', orient='index')

df_info_basicas = pd.json_normalize(df_vagas['informacoes_basicas'])
df_perfil_vaga = pd.json_normalize(df_vagas['perfil_vaga'])
df_beneficios = pd.json_normalize(df_vagas['beneficios'])

df_vagas = pd.concat([df_info_basicas, df_perfil_vaga, df_beneficios], axis=1)

df_vagas.tail()

df_vagas['data_requicisao'] = pd.to_datetime(df_vagas['data_requicisao'], format='%d-%m-%Y')
df_vagas['limite_esperado_para_contratacao'] = pd.to_datetime(df_vagas['limite_esperado_para_contratacao'], format='%d-%m-%Y', errors='coerce')
df_vagas['ano_publicacao'] = df_vagas['data_requicisao'].dt.year

# Conta a quantidade de vagas por ano de publicação
vagas_por_ano = df_vagas['ano_publicacao'].value_counts().sort_index()

# Cria o gráfico de barras
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=vagas_por_ano.index, y=vagas_por_ano.values)

# Adiciona os valores em cima das barras
for i, valor in enumerate(vagas_por_ano.values):
    ax.text(i, valor + 0.5, str(valor), ha='center', va='bottom', fontsize=10)

plt.xlabel('Ano de Publicação')
plt.ylabel('Quantidade de Vagas')
plt.title('Quantidade de Vagas por Ano de Publicação')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()




