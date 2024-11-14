import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Carregar os dados de Comércio
url_comercio = 'https://raw.githubusercontent.com/guilleunfv/tech-challenge-dados/main/data/raw/Comercio.csv'
df_comercio = pd.read_csv(url_comercio, encoding='utf-8', sep=';', engine='python')

# Carregar os dados de Produção
url_producao = 'https://raw.githubusercontent.com/guilleunfv/tech-challenge-dados/main/data/raw/Producao.csv'
df_producao = pd.read_csv(url_producao, encoding='utf-8', sep=';', engine='python')

# Transformar os dados de formato largo para formato longo
df_comercio_long = pd.melt(df_comercio, id_vars=['id', 'control', 'Produto'], var_name='Ano', value_name='Quantidade_Comercio')
df_producao_long = pd.melt(df_producao, id_vars=['id', 'control', 'produto'], var_name='Ano', value_name='Quantidade_Producao')

# Converter a coluna 'Ano' para numérico
df_comercio_long['Ano'] = pd.to_numeric(df_comercio_long['Ano'], errors='coerce')
df_producao_long['Ano'] = pd.to_numeric(df_producao_long['Ano'], errors='coerce')

# Eliminar linhas com 'Ano' nulo
df_comercio_long = df_comercio_long.dropna(subset=['Ano'])
df_producao_long = df_producao_long.dropna(subset=['Ano'])

# Filtrar os dados para os últimos 15 anos
ano_atual = datetime.datetime.now().year
ano_inicio = ano_atual - 15

df_comercio_long = df_comercio_long[df_comercio_long['Ano'] >= ano_inicio]
df_producao_long = df_producao_long[df_producao_long['Ano'] >= ano_inicio]

# Função para processar o DataFrame
def processar_dataframe(df, nome_produto):
    categoria = ''
    categorias = []
    subcategorias = []
    for index, row in df.iterrows():
        if pd.isna(row[nome_produto]):
            continue
        if row[nome_produto].isupper():
            categoria = row[nome_produto].title()
            subcategoria = ''
        else:
            subcategoria = row[nome_produto]
        categorias.append(categoria)
        subcategorias.append(subcategoria)
    df = df.assign(Categoria=categorias, Subcategoria=subcategorias)
    # Eliminar linhas que são categorias gerais
    df = df[df['Subcategoria'] != '']
    return df

# Processar os DataFrames
df_comercio_long = processar_dataframe(df_comercio_long, 'Produto')
df_producao_long = processar_dataframe(df_producao_long, 'produto')

# Padronizar nomes
df_comercio_long['Categoria'] = df_comercio_long['Categoria'].str.strip()
df_comercio_long['Subcategoria'] = df_comercio_long['Subcategoria'].str.strip()
df_producao_long['Categoria'] = df_producao_long['Categoria'].str.strip()
df_producao_long['Subcategoria'] = df_producao_long['Subcategoria'].str.strip()

# Substituir valores nulos por 0 em 'id' e quantidades
df_comercio_long['id'] = df_comercio_long['id'].fillna(0)
df_comercio_long['Quantidade_Comercio'] = df_comercio_long['Quantidade_Comercio'].fillna(0)

df_producao_long['id'] = df_producao_long['id'].fillna(0)
df_producao_long['Quantidade_Producao'] = df_producao_long['Quantidade_Producao'].fillna(0)

# Converter 'id' e quantidades para inteiros
df_comercio_long['id'] = df_comercio_long['id'].astype(int)
df_comercio_long['Quantidade_Comercio'] = df_comercio_long['Quantidade_Comercio'].astype(int)

df_producao_long['id'] = df_producao_long['id'].astype(int)
df_producao_long['Quantidade_Producao'] = df_producao_long['Quantidade_Producao'].astype(int)

# Unir os DataFrames
df_merged = pd.merge(df_comercio_long, df_producao_long, on=['Ano', 'Categoria', 'Subcategoria'], how='outer', suffixes=('_Comercio', '_Producao'))

# Preencher valores nulos com 0 nas quantidades
df_merged['Quantidade_Comercio'] = df_merged['Quantidade_Comercio'].fillna(0).astype(int)
df_merged['Quantidade_Producao'] = df_merged['Quantidade_Producao'].fillna(0).astype(int)

# Análise exploratória
df_tendencias = df_merged.groupby(['Ano', 'Categoria'])[['Quantidade_Comercio', 'Quantidade_Producao']].sum().reset_index()

# Visualização
for categoria in df_tendencias['Categoria'].unique():
    df_categoria = df_tendencias[df_tendencias['Categoria'] == categoria]
    plt.plot(df_categoria['Ano'], df_categoria['Quantidade_Producao'], label=categoria)

plt.xlabel('Ano')
plt.ylabel('Quantidade Produzida')
plt.title('Produção por Categoria nos Últimos 15 Anos')
plt.legend()
plt.show()

# Salvar dados processados
df_merged.to_csv('dados_processados_comercio_producao.csv', index=False)

