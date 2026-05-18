import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Chat Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Título
st.title("📊 Chat Analytics Dashboard")

st.write("Faça upload do arquivo CSV para análise.")

# Upload do arquivo
uploaded_file = st.file_uploader(
    "Escolha um arquivo CSV",
    type=["csv"]
)

# Verifica se o usuário enviou um arquivo
if uploaded_file is not None:

    try:
        # Leitura do CSV
        df = pd.read_csv(uploaded_file)

        st.success("Arquivo carregado com sucesso!")

        # Informações do dataset
        st.subheader("📌 Informações Gerais")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Linhas", df.shape[0])

        with col2:
            st.metric("Colunas", df.shape[1])

        with col3:
            st.metric("Valores Nulos", df.isnull().sum().sum())

        # Visualização dos dados
        st.subheader("📄 Pré-visualização dos Dados")

        st.dataframe(df)

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")