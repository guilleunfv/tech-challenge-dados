import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título e Introdução
st.title("Tech Challenge - Análise de Produção e Comércio de Vinhos")
st.markdown("### Integrantes do Grupo")
st.write("Rosicleia Cavalcante Mota")
st.write("Nathalia Dias Araujo")
st.write("Guillermo Jesus Camahuali Privat")
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

# Selección de años y productos
anos_disponiveis = comercio_df.columns[1:]  # Supondo que a primeira coluna é categoria, os demais são anos
produtos_disponiveis = comercio_df[comercio_df.columns[0]].unique()

ano_escolhido = st.selectbox("Selecione um ano para visualizar", anos_disponiveis)
produtos_escolhidos = st.multiselect("Selecione os produtos para comparação", produtos_disponiveis, default=produtos_disponiveis[:5])

# Filtragem de dados de comércio e produção
comercio_selecionado = comercio_df[comercio_df[comercio_df.columns[0]].isin(produtos_escolhidos)]
producao_selecionada = producao_df[producao_df[producao_df.columns[0]].isin(produtos_escolhidos)]

# Exibir tabela dinâmica
st.markdown("### Tabela de Comércio no Ano Selecionado")
st.write(comercio_selecionado[[comercio_df.columns[0], ano_escolhido]])

st.markdown("### Tabela de Produção no Ano Selecionado")
st.write(producao_selecionada[[producao_df.columns[0], ano_escolhido]])

# Gráfico de Barras para Comparação de Produtos no Ano Selecionado
fig, ax = plt.subplots()
ax.bar(comercio_selecionado[comercio_df.columns[0]], comercio_selecionado[ano_escolhido], label="Comércio", alpha=0.7)
ax.bar(producao_selecionada[producao_df.columns[0]], producao_selecionada[ano_escolhido], label="Produção", alpha=0.7)
ax.set_title(f"Comparação de Comércio e Produção de Vinhos em {ano_escolhido}")
ax.set_ylabel("Quantidade (Litros)")
ax.set_xlabel("Produto")
ax.legend()
st.pyplot(fig)

# Gráfico de Linha para Tendências ao Longo dos Anos
st.markdown("## Tendências ao Longo dos Anos")
anos_selecionados = st.multiselect("Selecione os anos para visualização da tendência", anos_disponiveis, default=anos_disponiveis[:5])

# Filtrar dados para os anos selecionados
comercio_tendencia = comercio_selecionado.set_index(comercio_df.columns[0])[anos_selecionados]
producao_tendencia = producao_selecionada.set_index(producao_df.columns[0])[anos_selecionados]

st.line_chart(comercio_tendencia)
st.line_chart(producao_tendencia)


