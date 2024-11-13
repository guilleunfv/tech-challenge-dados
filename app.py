import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
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

# Carregar os dados
comercio_df = pd.read_csv(url_comercio)
producao_df = pd.read_csv(url_producao)

# Verificar se existem colunas de 'categoria' e 'subcategoria'
if 'categoria' not in comercio_df.columns or 'subcategoria' not in comercio_df.columns:
    # Dividir a coluna 'produto' em 'categoria' e 'subcategoria'
    comercio_df['categoria'] = comercio_df['produto'].str.split(' - ', n=1).str[0]
    comercio_df['subcategoria'] = comercio_df['produto'].str.split(' - ', n=1).str[1]
    producao_df['categoria'] = producao_df['produto'].str.split(' - ', n=1).str[0]
    producao_df['subcategoria'] = producao_df['produto'].str.split(' - ', n=1).str[1]

# Mostrar a estrutura dos dados
st.markdown("### Dados de Comércio e Produção")
st.write("Abaixo estão os dados de comércio e produção carregados para análise.")

st.subheader("Dados de Comércio")
st.dataframe(comercio_df.head())

st.subheader("Dados de Produção")
st.dataframe(producao_df.head())

# Obter lista de anos disponíveis (assumindo que as colunas de anos consistem apenas de dígitos)
anos_disponiveis = [col for col in comercio_df.columns if col.isdigit()]

st.markdown("### Selecione o Ano, a Categoria e as Subcategorias para Comparação")

# Seleção do ano
ano_escolhido = st.selectbox("Selecione um ano para visualização:", anos_disponiveis)

# Seleção de categoria
categorias_disponiveis = sorted(comercio_df['categoria'].dropna().unique())
categoria_escolhida = st.selectbox("Selecione uma categoria:", categorias_disponiveis)

# Filtrar subcategorias com base na categoria selecionada
subcategorias_disponiveis = sorted(comercio_df[comercio_df['categoria'] == categoria_escolhida]['subcategoria'].dropna().unique())

# Verificar se há subcategorias disponíveis
if subcategorias_disponiveis:
    # Seleção de subcategorias
    subcategorias_escolhidas = st.multiselect("Selecione as subcategorias para comparação:", subcategorias_disponiveis, default=subcategorias_disponiveis[:5])
else:
    subcategorias_escolhidas = []
    st.write("Não há subcategorias disponíveis para esta categoria.")

# Filtrar dados de acordo com a categoria e subcategorias selecionadas
if subcategorias_escolhidas:
    comercio_selecionado = comercio_df[
        (comercio_df['categoria'] == categoria_escolhida) & 
        (comercio_df['subcategoria'].isin(subcategorias_escolhidas))
    ][['categoria', 'subcategoria', 'produto', ano_escolhido]]

    producao_selecionado = producao_df[
        (producao_df['categoria'] == categoria_escolhida) & 
        (producao_df['subcategoria'].isin(subcategorias_escolhidas))
    ][['categoria', 'subcategoria', 'produto', ano_escolhido]]
else:
    comercio_selecionado = comercio_df[
        (comercio_df['categoria'] == categoria_escolhida)
    ][['categoria', 'subcategoria', 'produto', ano_escolhido]]

    producao_selecionado = producao_df[
        (producao_df['categoria'] == categoria_escolhida)
    ][['categoria', 'subcategoria', 'produto', ano_escolhido]]

# Mesclar dados para exibir lado a lado
dados_comparacao = pd.merge(
    comercio_selecionado, 
    producao_selecionado, 
    on=['categoria', 'subcategoria', 'produto'], 
    suffixes=('_Comércio', '_Produção')
)

st.markdown("### Tabela de Comparação de Comércio e Produção")
st.write("A tabela abaixo mostra uma comparação entre os valores de comércio e produção para as seleções feitas no ano escolhido.")
st.dataframe(dados_comparacao)

# Verificar se há dados para exibir
if not dados_comparacao.empty:
    # Gráfico de Barras Agrupadas para Comparação
    st.markdown("## Comparação Visual de Comércio e Produção no Ano Selecionado")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    largura = 0.35  # Largura das barras
    
    # Índices para as barras
    indices = range(len(dados_comparacao))
    
    # Converter valores para numéricos (caso sejam strings)
    dados_comparacao[ano_escolhido + '_Comércio'] = pd.to_numeric(dados_comparacao[ano_escolhido + '_Comércio'], errors='coerce')
    dados_comparacao[ano_escolhido + '_Produção'] = pd.to_numeric(dados_comparacao[ano_escolhido + '_Produção'], errors='coerce')
    
    # Substituir NaN por 0
    dados_comparacao[ano_escolhido + '_Comércio'] = dados_comparacao[ano_escolhido + '_Comércio'].fillna(0)
    dados_comparacao[ano_escolhido + '_Produção'] = dados_comparacao[ano_escolhido + '_Produção'].fillna(0)
    
    # Plotar barras lado a lado
    ax.bar(indices, dados_comparacao[ano_escolhido + '_Comércio'], largura, label='Comércio', color='skyblue')
    ax.bar([i + largura for i in indices], dados_comparacao[ano_escolhido + '_Produção'], largura, label='Produção', color='salmon')
    
    # Títulos e etiquetas
    ax.set_xlabel("Produtos")
    ax.set_ylabel("Quantidade (Litros)")
    ax.set_title(f"Comparação entre Comércio e Produção de Vinhos em {ano_escolhido}")
    ax.set_xticks([i + largura / 2 for i in indices])
    ax.set_xticklabels(dados_comparacao['produto'], rotation=45)
    ax.legend()
    
    st.pyplot(fig)
    
    # Explicação em português
    st.markdown("### Explicação dos Gráficos e Dados")
    st.write("""
    Esses gráficos comparam as quantidades de comércio e produção dos produtos selecionados para o ano escolhido. 
    As barras azuis representam o comércio, enquanto as barras vermelhas mostram a produção. 
    Se a produção é maior do que o comércio, pode-se observar uma maior retenção no mercado interno ou nos estoques. 
    Esses insights são úteis para entender a dinâmica entre o que é produzido e o que é efetivamente comercializado.
    """)
else:
    st.write("Não há dados disponíveis para as seleções feitas.")

# Gráfico de Linha para Visualizar Tendência ao Longo dos Anos
st.markdown("## Tendência Anual")

anos_selecionados = st.multiselect("Selecione os anos para a visualização de tendência:", anos_disponiveis, default=anos_disponiveis[:5])

if anos_selecionados:
    # Filtrar dados para os anos selecionados
    if subcategorias_escolhidas:
        comercio_tendencia = comercio_df[
            (comercio_df['categoria'] == categoria_escolhida) &
            (comercio_df['subcategoria'].isin(subcategorias_escolhidas))
        ].set_index('produto')[anos_selecionados]
        
        producao_tendencia = producao_df[
            (producao_df['categoria'] == categoria_escolhida) &
            (producao_df['subcategoria'].isin(subcategorias_escolhidas))
        ].set_index('produto')[anos_selecionados]
    else:
        comercio_tendencia = comercio_df[
            (comercio_df['categoria'] == categoria_escolhida)
        ].set_index('produto')[anos_selecionados]
        
        producao_tendencia = producao_df[
            (producao_df['categoria'] == categoria_escolhida)
        ].set_index('produto')[anos_selecionados]
    
    st.markdown("### Comércio - Tendência Anual")
    st.line_chart(comercio_tendencia.T)
    
    st.markdown("### Produção - Tendência Anual")
    st.line_chart(producao_tendencia.T)
    
    st.markdown("### Explicação da Tendência Anual")
    st.write("""
    Os gráficos de linha exibem a tendência anual de comércio e produção para os produtos selecionados.
    Essa visualização é útil para identificar mudanças ao longo do tempo, como crescimento ou diminuição das atividades de comércio e produção. 
    Essas tendências são essenciais para uma análise estratégica e projeções futuras no setor de vinhos.
    """)
else:
    st.write("Selecione pelo menos um ano para visualizar a tendência anual.")
