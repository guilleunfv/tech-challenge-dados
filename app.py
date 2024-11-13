import streamlit as st
import pandas as pd

# Título e Introdução
st.title("Tech Challenge - Análise de Produção e Comércio de Vinhos 🍇")
st.markdown("### Integrantes do Grupo")
st.write("Rosicleia Cavalcante Mota")
st.write("Nathalia Dias Araujo")
st.write("Guillermo Jesus Camahuali Privat")
st.write("Kelly Priscilla Matos Campos")

st.markdown("## Introdução")
st.write("""
Esta aplicação apresenta uma análise detalhada da produção e do comércio de vinhos nos últimos anos, com foco nas tendências e comparações entre diferentes categorias e subcategorias.
Utilizamos um dataset combinado de produção e comércio para facilitar a visualização.
""")

# Carregar o dataset
url = 'https://drive.google.com/uc?id=1Lj8cV5j8GBRKOOHBcgPzYhXp7TMp_9kT'  # Link direto para download
df = pd.read_csv(url)

# Configurações de filtros interativos
st.sidebar.header("Filtros")
anos = sorted(df['Ano'].unique())
categorias = sorted(df['CATEGORIA'].unique())
subcategorias = sorted(df['SUBCATEGORIA'].unique())

ano_selecionado = st.sidebar.multiselect("Selecione o(s) Ano(s)", anos, default=anos)
categoria_selecionada = st.sidebar.multiselect("Selecione a(s) Categoria(s)", categorias, default=categorias)
subcategoria_selecionada = st.sidebar.multiselect("Selecione a(s) Subcategoria(s)", subcategorias, default=subcategorias)

# Filtrar o DataFrame com base nas seleções
df_filtrado = df[
    (df['Ano'].isin(ano_selecionado)) & 
    (df['CATEGORIA'].isin(categoria_selecionada)) & 
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

# Explicação e insights
st.markdown("## Conclusão")
st.write("""
A análise interativa acima permite observar a evolução da produção e do comércio de vinhos ao longo dos anos, facilitando comparações por categoria e subcategoria.
Com os filtros aplicados, é possível identificar tendências específicas e entender melhor o comportamento do setor de vinhos no Brasil.
""")
