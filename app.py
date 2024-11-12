import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título e Introdução
st.title("Tech Challenge - Análise de Produção e Comércio de Vinhos")
st.markdown("### Integrantes do Grupo")
st.write("Rosicleia Cavalcante Mota")
st.write("Nathalia Dias Araujo")
st.write("Guillermo Jesus Camahuali Privat")
st.write("Andressa Leonilia Da Silva Gomes")
st.write("Kelly Priscilla Matos Campos")

st.markdown("## Introdução")
st.write("Esta aplicação apresenta uma análise detalhada da produção e do comércio de vinhos nos últimos anos.")

# Carregar os Dados diretamente do Google Drive
url_comercio = "https://drive.google.com/uc?export=download&id=1f6lHD3fjVLtkyWtP7CgY2vplfAJ9mAkN"
url_producao = "https://drive.google.com/uc?export=download&id=1uAoGAH8w_nYWSmv1IJBtTKfJzWgwPzsc"

comercio_df = pd.read_csv(url_comercio)
producao_df = pd.read_csv(url_producao)

# Exibir dados
st.markdown("### Dados de Comércio")
st.write(comercio_df.head())

st.markdown("### Dados de Produção")
st.write(producao_df.head())

# Análise Descritiva
st.markdown("## Análise Descritiva")
st.write("### Estatísticas de Comércio")
st.write(comercio_df.describe())
    
st.write("### Estatísticas de Produção")
st.write(producao_df.describe())

# Gráfico de Linha para Tendências Anuais
st.markdown("## Gráfico de Linha - Tendência Anual")
anos = comercio_df.columns[1:]  # Supondo que a primeira coluna é uma categoria e o restante são anos
st.line_chart(comercio_df.set_index(comercio_df.columns[0])[anos])
st.line_chart(producao_df.set_index(producao_df.columns[0])[anos])

# Gráfico de Barras para Comparação Anual
st.markdown("## Gráfico de Barras - Comparação Anual")
ano_escolhido = st.selectbox("Selecione um ano para comparar", anos)
fig, ax = plt.subplots()
ax.bar(comercio_df[comercio_df.columns[0]], comercio_df[ano_escolhido])
ax.set_title(f"Comércio de Vinhos em {ano_escolhido}")
ax.set_ylabel("Quantidade (Litros)")
ax.set_xlabel("Categoria")
st.pyplot(fig)

fig, ax = plt.subplots()
ax.bar(producao_df[producao_df.columns[0]], producao_df[ano_escolhido], color='orange')
ax.set_title(f"Produção de Vinhos em {ano_escolhido}")
ax.set_ylabel("Quantidade (Litros)")
ax.set_xlabel("Categoria")
st.pyplot(fig)

# Gráfico de Pizza para Distribuição
st.markdown("## Gráfico de Pizza - Distribuição por Categoria")
fig, ax = plt.subplots()
ax.pie(comercio_df[ano_escolhido], labels=comercio_df[comercio_df.columns[0]], autopct='%1.1f%%')
ax.set_title(f"Distribuição do Comércio de Vinhos em {ano_escolhido}")
st.pyplot(fig)

fig, ax = plt.subplots()
ax.pie(producao_df[ano_escolhido], labels=producao_df[producao_df.columns[0]], autopct='%1.1f%%')
ax.set_title(f"Distribuição da Produção de Vinhos em {ano_escolhido}")
st.pyplot(fig)

