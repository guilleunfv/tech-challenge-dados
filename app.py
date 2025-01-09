import openai
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuração da chave API da OpenAI
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Estilo personalizado com CSS
st.markdown("""
    <style>
    .header {
        background-color: #8B0000;
        padding: 10px;
        border-radius: 5px;
    }
    .header h1 {
        color: #ffffff;
        font-family: 'Arial Black', sans-serif;
        text-align: center;
    }
    .header p {
        color: #F5F5DC;
        text-align: center;
        font-size: 18px;
    }
    .bot-container {
        border: 2px solid #8B0000;
        background-color: #F5F5F5;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título e cabeçalho
st.markdown('<div class="header"><h1>Análise de Dados de Exportação de Vinhos</h1><p>Bah! Wine Gaúchos Exportadora</p></div>', unsafe_allow_html=True)

# Função para interação com o ChatGPT
def perguntar_a_chatgpt(pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em análise de dados, especialmente na área de exportação de vinhos brasileiros."},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro ao conectar com o ChatGPT: {e}"

# Chat na cabeceira
st.markdown('<div class="bot-container"><h3>Bem-vindo ao BahBot Vinícola!</h3><p>Faça perguntas sobre os dados de exportação ou solicite análises.</p></div>', unsafe_allow_html=True)
pergunta = st.text_input("Digite sua pergunta ou solicitação:")
if st.button("Enviar"):
    if pergunta:
        resposta = perguntar_a_chatgpt(pergunta)
        st.markdown("### Resposta do BahBot:")
        st.write(resposta)
    else:
        st.write("Por favor, digite uma pergunta válida.")

# Carga dos dados
@st.cache_data
def carregar_dados():
    url = "https://drive.google.com/uc?id=1-mrtTLjOPh_XVk1mkDH00SUJxWkuOu5o"
    dados = pd.read_csv(url, delimiter=';', encoding='utf-8', quotechar='"')
    dados.columns = dados.columns.str.strip()
    return dados

df = carregar_dados()

# Visualização inicial dos dados
st.markdown("### Dados Gerais de Exportação de Vinhos")
st.dataframe(df)

# Filtros interativos
st.sidebar.header("Filtros Interativos")

anos = st.sidebar.multiselect("Selecione os Anos", df['Año'].unique(), default=df['Año'].unique())
df_filtrado = df[df['Año'].isin(anos)]

paises = st.sidebar.multiselect("Selecione os Países", df['País'].unique(), default=df['País'].unique()[:10])
df_filtrado = df_filtrado[df_filtrado['País'].isin(paises)]

st.markdown("### Dados Filtrados")
st.dataframe(df_filtrado)

# Gráficos relevantes
st.markdown("## Gráficos de Análise")
st.markdown("### Tendência de Exportação (US$ FOB por Ano)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_filtrado.groupby('Año')['Valor US$ FOB'].sum(), color='#8B0000')
ax.set_title("Tendência de Exportação de Vinhos", fontsize=16, color='#8B0000')
ax.set_xlabel("Ano", fontsize=14)
ax.set_ylabel("Valor Total (US$ FOB)", fontsize=14)
st.pyplot(fig)

st.markdown("### Exportação por País")
fig, ax = plt.subplots(figsize=(10, 6))
df_filtrado.groupby('País')['Valor US$ FOB'].sum().sort_values(ascending=False).head(10).plot(kind='bar', color='#A52A2A', ax=ax)
ax.set_title("Top 10 Países de Destino", fontsize=16, color='#8B0000')
ax.set_xlabel("País", fontsize=14)
ax.set_ylabel("Valor Total (US$ FOB)", fontsize=14)
st.pyplot(fig)
