import pandas as pd

# Carregar os arquivos originais
df_producao = pd.read_excel('data/raw/producao1.xlsx')
df_comercio = pd.read_excel('data/raw/Comercio1.csv.xlsx')

# Transformar os dados para o formato longo usando melt, mantendo "Ano" como uma coluna de valores
df_producao_melted = df_producao.melt(id_vars=["CATEGORIA", "SUBCATEGORIA"], 
                                      var_name="Ano", value_name="Producao")
df_comercio_melted = df_comercio.melt(id_vars=["CATEGORIA", "SUBCATEGORIA"], 
                                      var_name="Ano", value_name="Comercio")

# Unir os DataFrames de produção e comércio em um único DataFrame usando as colunas comuns
df_combined = pd.merge(df_producao_melted, df_comercio_melted, 
                       on=["CATEGORIA", "SUBCATEGORIA", "Ano"], how="outer")

# Conversão de tipos para remover o ".0"
df_combined['Ano'] = df_combined['Ano'].astype(int)  # Convertendo o ano para int
df_combined['Producao'] = df_combined['Producao'].fillna(0).astype(int)  # Convertendo produção para int
df_combined['Comercio'] = df_combined['Comercio'].fillna(0).astype(int)  # Convertendo comércio para int

# Salvar o DataFrame combinado como CSV na pasta cleaned para análise futura
df_combined.to_csv('data/cleaned/producao_comercio_combined.csv', index=False)
