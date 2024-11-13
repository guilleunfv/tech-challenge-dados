import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configura o layout da página
st.set_page_config(page_title="Tech Challenge - Análise de Vinhos", layout="centered")

# Título e Introdução
st.title("Tech Challenge - Análise de Produção e Comércio de Vinhos 🍇")
st.markdown("### Integrantes do Grupo")
st.write("Rosicleia Cavalcante Mota")
st.write("Nathalia Dias Araujo")
st.write("Guillermo Jesus Camahuali Privat")
st.write("Kelly Priscilla Matos Campos")

st.markdown("## Introdução")
st.write("Esta aplicação apresenta uma análise detalhada da produção e do comércio de vinhos nos últimos anos, com foco nas tendências e comparações entre diferentes categorias e subcategorias.")

# Carregar os Dados diretamente do Google Drive
url_comercio = "https://drive.google.com/uc?export=download&id=1f6lHD3fjVLtkyWtP7CgY2vplfAJ9mAkN"
url_producao = "https://drive.google.com/uc?export=download&id=1uAoGAH8w_nYWSmv1IJBtTKfJzWgwPzsc"

comercio_df = pd.read_csv(url_comercio)
producao_df = pd.read_csv(url_producao)

# Exibir dados
st.markdown("### Dados de Comércio e Produção")
st.write("Abaixo estão os dados de comércio e produção carregados para análise.")

st.subheader("Dados de Comércio")
st.dataframe(comercio_df.head())

st.subheader("Dados de Produção")
st.dataframe(producao_df.head())

# Seleção de Ano e Produtos para comparação
anos_disponiveis = comercio_df.columns[1:]  # Supondo que a primeira coluna é categoria, os demais são anos
produtos_disponiveis = sorted(comercio_df[comercio_df.columns[0]].unique())

st.markdown("### Selecione o Ano e os Produtos para Comparação")

# Widgets para seleção
ano_escolhido = st.selectbox("Selecione um ano para visualização:", anos_disponiveis)
produtos_escolhidos = st.multiselect("Selecione as categorias e subcategorias para comparação:", produtos_disponiveis, default=produtos_disponiveis[:5])

# Filtrar dados de acordo com o ano e produtos selecionados
comercio_selecionado = comercio_df[comercio_df[comercio_df.columns[0]].isin(produtos_escolhidos)][[comercio_df.columns[0], ano_escolhido]]
producao_selecionado = producao_df[producao_df[producao_df.columns[0]].isin(produtos_escolhidos)][[producao_df.columns[0], ano_escolhido]]

# Mesclar dados para exibir lado a lado
dados_comparacao = pd.merge(comercio_selecionado, producao_selecionado, on=comercio_df.columns[0], suffixes=('_Comércio', '_Produção'))
st.markdown("### Tabela de Comparação de Comércio e Produção")
st.write("A tabela abaixo mostra uma comparação entre os valores de comércio e produção para as categorias e subcategorias selecionadas no ano escolhido.")
st.dataframe(dados_comparacao)

# Gráfico de Barras Agrupadas para Comparação
st.markdown("## Comparação Visual de Comércio e Produção no Ano Selecionado")

fig, ax = plt.subplots(figsize=(10, 6))
largura = 0.35  # largura das barras

# Índices para as barras
indices = range(len(dados_comparacao))

# Plotar barras lado a lado
ax.bar(indices, dados_comparacao[f"{ano_escolhido}_Comércio"], largura, label='Comércio', color='skyblue')
ax.bar([i + largura for i in indices], dados_comparacao[f"{ano_escolhido}_Produção"], largura, label='Produção', color='salmon')

# Títulos e etiquetas
ax.set_xlabel("Categorias/Subcategorias")
ax.set_ylabel("Quantidade (Litros)")
ax.set_title(f"Comparação entre Comércio e Produção de Vinhos em {ano_escolhido}")
ax.set_xticks([i + largura / 2 for i in indices])
ax.set_xticklabels(dados_comparacao[comercio_df.columns[0]], rotation=45)
ax.legend()

st.pyplot(fig)

# Explicação em português
st.markdown("### Explicação dos Gráficos e Dados")
st.write("""
Esses gráficos comparam as quantidades de comércio e produção das categorias e subcategorias selecionadas para o ano escolhido. 
As barras azuis representam o comércio, enquanto as barras vermelhas mostram a produção. 
Se a produção é maior do que o comércio, pode-se observar uma maior retenção no mercado interno ou nos estoques. 
Esses insights são úteis para entender a dinâmica entre o que é produzido e o que é efetivamente comercializado.
""")

# Gráfico de Linha para Visualizar Tendência ao Longo dos Anos
st.markdown("## Tendência Anual")
anos_selecionados = st.multiselect("Selecione os anos para a visualização de tendência:", anos_disponiveis, default=anos_disponiveis[:5])

# Verificação para evitar erro quando não há anos selecionados
if anos_selecionados:
    # Filtrar dados para os anos selecionados
    comercio_tendencia = comercio_df[comercio_df[comercio_df.columns[0]].isin(produtos_escolhidos)].set_index(comercio_df.columns[0])[anos_selecionados]
    producao_tendencia = producao_df[producao_df[producao_df.columns[0]].isin(produtos_escolhidos)].set_index(producao_df.columns[0])[anos_selecionados]

    st.markdown("### Comércio - Tendência Anual")
    st.line_chart(comercio_tendencia)

    st.markdown("### Produção - Tendência Anual")
    st.line_chart(producao_tendencia)

st.markdown("### Explicação da Tendência Anual")
st.write("""
Os gráficos de linha exibem a tendência anual de comércio e produção para as categorias e subcategorias selecionadas.
Essa visualização é útil para identificar mudanças ao longo do tempo, como crescimento ou diminuição das atividades de comércio e produção. 
Essas tendências são essenciais para uma análise estratégica e projeções futuras no setor de vinhos.
""")

