import streamlit as st
import pandas as pd

# Carregar o dataset
url = 'https://drive.google.com/uc?id=1Lj8cV5j8GBRKOOHBcgPzYhXp7TMp_9kT'  # Link direto para download
df = pd.read_csv(url)

# Asegurar que 'Ano' sea interpretado como entero
df['Ano'] = df['Ano'].astype(int)

# Configurações de filtros interativos
st.sidebar.header("Filtros")
anos = sorted(df['Ano'].unique())
categorias = sorted(df['CATEGORIA'].unique())

# Filtro para o ano e a categoria
ano_selecionado = st.sidebar.multiselect("Selecione o(s) Ano(s)", anos, default=anos)
categoria_selecionada = st.sidebar.selectbox("Selecione a Categoria", categorias)

# Filtrar subcategorias com base na categoria selecionada
subcategorias_filtradas = df[df['CATEGORIA'] == categoria_selecionada]['SUBCATEGORIA'].unique()
subcategoria_selecionada = st.sidebar.multiselect("Selecione a(s) Subcategoria(s)", sorted(subcategorias_filtradas), default=subcategorias_filtradas)

# Filtrar o DataFrame com base nas seleções
df_filtrado = df[
    (df['Ano'].isin(ano_selecionado)) & 
    (df['CATEGORIA'] == categoria_selecionada) & 
    (df['SUBCATEGORIA'].isin(subcategoria_selecionada))
]

# Visualização de dados filtrados
st.markdown("## Dados Filtrados")
st.dataframe(df_filtrado)

# Gráficos interativos
st.markdown("## Análise Gráfica")

# Gráfico de Produção por Ano
st.subheader("Produção por Ano")
grafico_producao = df_filtrado.groupby('Ano')['Producao'].sum()
st.line_chart(grafico_producao)

# Gráfico de Comércio por Ano
st.subheader("Comércio por Ano")
grafico_comercio = df_filtrado.groupby('Ano')['Comercio'].sum()
st.line_chart(grafico_comercio)

# Comparação entre Produção e Comércio
st.subheader("Comparação entre Produção e Comércio")
grafico_comparacao = df_filtrado.groupby('Ano')[['Producao', 'Comercio']].sum()
st.line_chart(grafico_comparacao)
