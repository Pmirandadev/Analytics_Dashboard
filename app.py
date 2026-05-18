import streamlit as st
import pandas as pd
import plotly.express as px

from utils.tratamento import (
    limpar_dados,
    relatorio_qualidade
)

# ==================================
# CONFIGURAÇÃO
# ==================================

st.set_page_config(
    page_title="Chat Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================
# TÍTULO
# ==================================

st.title("📊 Chat Analytics Dashboard")

st.write("Upload e análise inteligente de dados.")

# ==================================
# UPLOAD
# ==================================

uploaded_file = st.file_uploader(
    "Escolha um arquivo CSV",
    type=["csv"]
)

# ==================================
# PROCESSAMENTO
# ==================================

if uploaded_file is not None:

    try:

        # ==========================
        # LEITURA CSV
        # ==========================

        df = pd.read_csv(uploaded_file)

        # ==========================
        # LIMPEZA
        # ==========================

        df = limpar_dados(df)

        st.success("Arquivo carregado com sucesso!")

        # ==========================
        # SIDEBAR
        # ==========================

        st.sidebar.header("🔎 Filtros")

        df_filtrado = df.copy()

        colunas_categoricas = df.select_dtypes(
            include="object"
        ).columns.tolist()

        for coluna in colunas_categoricas:

            valores = sorted(
                df[coluna].dropna().unique()
            )

            selecao = st.sidebar.multiselect(
                f"Filtrar {coluna}",
                valores
            )

            if selecao:
                df_filtrado = df_filtrado[
                    df_filtrado[coluna].isin(selecao)
                ]

        # ==========================
        # KPIs
        # ==========================

        st.subheader("📌 Indicadores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Registros",
                df_filtrado.shape[0]
            )

        with col2:
            st.metric(
                "Colunas",
                df_filtrado.shape[1]
            )

        with col3:
            st.metric(
                "Nulos",
                df_filtrado.isnull().sum().sum()
            )

        with col4:
            st.metric(
                "Duplicados",
                df_filtrado.duplicated().sum()
            )

        st.divider()

        # ==========================
        # RELATÓRIO QUALIDADE
        # ==========================

        st.subheader("🧹 Qualidade dos Dados")

        qualidade = relatorio_qualidade(df_filtrado)

        st.dataframe(
            qualidade,
            use_container_width=True
        )

        st.divider()

        # ==========================
        # VISUALIZAÇÕES
        # ==========================

        st.subheader("📈 Visualizações")

        coluna_grafico = st.selectbox(
            "Escolha uma coluna",
            colunas_categoricas
        )

        contagem = df_filtrado[
            coluna_grafico
        ].value_counts().reset_index()

        contagem.columns = [
            coluna_grafico,
            "Quantidade"
        ]

        col_graf1, col_graf2 = st.columns(2)

        # ==========================
        # BARRAS
        # ==========================

        with col_graf1:

            fig_bar = px.bar(
                contagem,
                x=coluna_grafico,
                y="Quantidade",
                title=f"{coluna_grafico}"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

        # ==========================
        # PIZZA
        # ==========================

        with col_graf2:

            fig_pizza = px.pie(
                contagem,
                names=coluna_grafico,
                values="Quantidade",
                title=f"{coluna_grafico}"
            )

            st.plotly_chart(
                fig_pizza,
                use_container_width=True
            )

        st.divider()

        # ==========================
        # TABELA
        # ==========================

        st.subheader("📄 Dados")

        st.dataframe(
            df_filtrado,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Erro: {e}")