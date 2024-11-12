import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Tech Challenge - Análise de Produção e Comércio de Vinhos')
st.write("Por favor, carregue os dois arquivos CSV para continuar.")

# Upload dos arquivos CSV
uploaded_comercio = st.file_uploader("Escolha o arquivo de comércio", type=['csv'])
uploaded_producao = st.file_uploader("Escolha o arquivo de produção", type=['csv'])

if uploaded_comercio is not None and uploaded_producao is not None:
    # Carregar os arquivos em DataFrames
    df_comercio = pd.read_csv(uploaded_comercio)
    df_producao = pd.read_csv(uploaded_producao)

    # Verificar colunas carregadas
    st.write("Colunas carregadas do arquivo de comércio:")
    st.write(df_comercio.columns)
    st.write("Colunas carregadas do arquivo de produção:")
    st.write(df_producao.columns)

    # Definindo os anos corretamente com base nos nomes das colunas
    anos = ['Quantidade_Litros_2009', 'Quantidade_Litros_2010', 'Quantidade_Litros_2011', 
            'Quantidade_Litros_2012', 'Quantidade_Litros_2013', 'Quantidade_Litros_2014', 
            'Quantidade_Litros_2015', 'Quantidade_Litros_2016', 'Quantidade_Litros_2017', 
            'Quantidade_Litros_2018', 'Quantidade_Litros_2019', 'Quantidade_Litros_2020', 
            'Quantidade_Litros_2021', 'Quantidade_Litros_2022', 'Quantidade_Litros_2023']

    # Verificar se os anos estão presentes no DataFrame de comércio
    if all(ano in df_comercio.columns for ano in anos):
        # Gráfico de Comércio
        st.header("Tendência de Comércio de Vinhos")
        fig_comercio, ax_comercio = plt.subplots()
        for produto in df_comercio['produto'].unique():
            ax_comercio.plot(anos, df_comercio[df_comercio['produto'] == produto][anos].values.flatten(), label=produto)
        ax_comercio.set_title("Tendência de Comércio de Vinhos ao Longo dos Anos")
        ax_comercio.set_xlabel("Anos")
        ax_comercio.set_ylabel("Quantidade em Litros")
        ax_comercio.legend()
        st.pyplot(fig_comercio)
    else:
        st.error("Os nomes das colunas de anos no arquivo de comércio não coincidem com o esperado.")

    # Verificar se os anos estão presentes no DataFrame de produção
    if all(ano in df_producao.columns for ano in anos):
        # Gráfico de Produção
        st.header("Tendência de Produção de Vinhos")
        fig_producao, ax_producao = plt.subplots()
        for produto in df_producao['produto'].unique():
            ax_producao.plot(anos, df_producao[df_producao['produto'] == produto][anos].values.flatten(), label=produto)
        ax_producao.set_title("Tendência de Produção de Vinhos ao Longo dos Anos")
        ax_producao.set_xlabel("Anos")
        ax_producao.set_ylabel("Quantidade em Litros")
        ax_producao.legend()
        st.pyplot(fig_producao)
    else:
        st.error("Os nomes das colunas de anos no arquivo de produção não coincidem com o esperado.")
