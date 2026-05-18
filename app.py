import streamlit as st
import pandas as pd
import plotly.express as px

# ===================================
# CONFIGURAÇÃO DA PÁGINA
# ===================================

st.set_page_config(
    page_title="Chat Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ===================================
# TÍTULO
# ===================================

st.title("📊 Chat Analytics Dashboard")

st.write("Faça upload do arquivo CSV para análise.")

# ===================================
# UPLOAD CSV
# ===================================

uploaded_file = st.file_uploader(
    "Escolha um arquivo CSV",
    type=["csv"]
)

# ===================================
# PROCESSAMENTO
# ===================================

if uploaded_file is not None:

    try:

        # ============================
        # LEITURA CSV
        # ============================

        df = pd.read_csv(uploaded_file)

        st.success("Arquivo carregado com sucesso!")

        # ============================
        # SIDEBAR
        # ============================

        st.sidebar.header("🔎 Filtros")

        df_filtrado = df.copy()

        # Colunas categóricas
        colunas_categoricas = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        # Filtros dinâmicos
        for coluna in colunas_categoricas:

            valores_unicos = sorted(
                df[coluna].dropna().unique()
            )

            selecao = st.sidebar.multiselect(
                f"Filtrar {coluna}",
                valores_unicos
            )

            if selecao:
                df_filtrado = df_filtrado[
                    df_filtrado[coluna].isin(selecao)
                ]

        # ============================
        # KPIs
        # ============================

        st.subheader("📌 Indicadores")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total de Registros",
                df_filtrado.shape[0]
            )

        with col2:
            st.metric(
                "Total de Colunas",
                df_filtrado.shape[1]
            )

        with col3:
            st.metric(
                "Valores Nulos",
                df_filtrado.isnull().sum().sum()
            )

        st.divider()

        # ============================
        # GRÁFICOS
        # ============================

        st.subheader("📈 Visualizações")

        # Seleção de colunas
        coluna_grafico = st.selectbox(
            "Escolha uma coluna para análise",
            colunas_categoricas
        )

        # Contagem
        contagem = df_filtrado[coluna_grafico] \
            .value_counts() \
            .reset_index()

        contagem.columns = [
            coluna_grafico,
            "Quantidade"
        ]

        # Layout dos gráficos
        col_graf1, col_graf2 = st.columns(2)

        # ============================
        # GRÁFICO DE BARRAS
        # ============================

        with col_graf1:

            fig_bar = px.bar(
                contagem,
                x=coluna_grafico,
                y="Quantidade",
                title=f"Distribuição por {coluna_grafico}",
                text_auto=True
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

        # ============================
        # GRÁFICO DE PIZZA
        # ============================

        with col_graf2:

            fig_pizza = px.pie(
                contagem,
                names=coluna_grafico,
                values="Quantidade",
                title=f"Percentual por {coluna_grafico}"
            )

            st.plotly_chart(
                fig_pizza,
                use_container_width=True
            )

        st.divider()

        # ============================
        # TABELA
        # ============================

        st.subheader("📄 Dados Filtrados")

        st.dataframe(
            df_filtrado,
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")