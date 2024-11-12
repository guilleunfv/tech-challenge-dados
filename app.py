import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Tech Challenge - Análise de Produção e Comércio de Vinhos")

# Cargar los datos
st.sidebar.header("Upload dos Arquivos CSV")
uploaded_comercio = st.sidebar.file_uploader("Escolha o arquivo de comércio", type=["csv"])
uploaded_producao = st.sidebar.file_uploader("Escolha o arquivo de produção", type=["csv"])

if uploaded_comercio and uploaded_producao:
    # Leitura dos CSVs
    df_comercio = pd.read_csv(uploaded_comercio)
    df_producao = pd.read_csv(uploaded_producao)
    
    # Mostrar os dados
    st.write("### Dados de Comércio")
    st.write(df_comercio.head())
    
    st.write("### Dados de Produção")
    st.write(df_producao.head())
    
    # Análise dos Dados
    st.header("Análise de Comércio e Produção")
    
    # Mostrar gráfico de comércio
    st.subheader("Tendência do Comércio de Vinhos")
    anos = [str(ano) for ano in range(2009, 2024)]
    for produto in df_comercio['produto'].unique():
        plt.figure(figsize=(10, 5))
        plt.plot(anos, df_comercio[df_comercio['produto'] == produto][anos].values.flatten(), label=produto)
        plt.xlabel("Ano")
        plt.ylabel("Quantidade de Litros")
        plt.title(f"Tendência do Comércio: {produto}")
        plt.legend()
        st.pyplot(plt)

    # Mostrar gráfico de produção
    st.subheader("Tendência da Produção de Vinhos")
    for produto in df_producao['produto'].unique():
        plt.figure(figsize=(10, 5))
        plt.plot(anos, df_producao[df_producao['produto'] == produto][anos].values.flatten(), label=produto)
        plt.xlabel("Ano")
        plt.ylabel("Quantidade de Litros")
        plt.title(f"Tendência da Produção: {produto}")
        plt.legend()
        st.pyplot(plt)
else:
    st.write("Por favor, carregue os dois arquivos CSV para continuar.")