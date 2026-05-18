import streamlit as st
import pandas as pd

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="Chat Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# TÍTULO
# =========================

st.title("📊 Chat Analytics Dashboard")

st.write("Faça upload do arquivo CSV para análise.")

# =========================
# UPLOAD CSV
# =========================

uploaded_file = st.file_uploader(
    "Escolha um arquivo CSV",
    type=["csv"]
)

# =========================
# PROCESSAMENTO
# =========================

if uploaded_file is not None:

    try:
        # Leitura CSV
        df = pd.read_csv(uploaded_file)

        st.success("Arquivo carregado com sucesso!")

        # =========================
        # SIDEBAR
        # =========================

        st.sidebar.header("🔎 Filtros")

        # Cria cópia do dataframe
        df_filtrado = df.copy()

        # Seleciona colunas categóricas
        colunas_categoricas = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        # Criação dinâmica dos filtros
        for coluna in colunas_categoricas:

            valores_unicos = sorted(
                df[coluna].dropna().unique()
            )

            selecao = st.sidebar.multiselect(
                f"Filtrar {coluna}",
                valores_unicos
            )

            # Aplicação do filtro
            if selecao:
                df_filtrado = df_filtrado[
                    df_filtrado[coluna].isin(selecao)
                ]

        # =========================
        # MÉTRICAS
        # =========================

        st.subheader("📌 Informações Gerais")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Linhas", df_filtrado.shape[0])

        with col2:
            st.metric("Colunas", df_filtrado.shape[1])

        with col3:
            st.metric(
                "Valores Nulos",
                df_filtrado.isnull().sum().sum()
            )

        # =========================
        # TABELA
        # =========================

        st.subheader("📄 Dados Filtrados")

        st.dataframe(
            df_filtrado,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")