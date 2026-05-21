import streamlit as st
import pandas as pd
import plotly.express as px

from utils.time_series import (
    detectar_datas,
    agrupar_periodo
)

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="Time Series Analytics",
    page_icon="📅",
    layout="wide"
)

# =====================================
# TÍTULO
# =====================================

st.title("📅 Time Series Analytics")

st.write(
    "Análise temporal dinâmica dos datasets."
)

# =====================================
# UPLOAD
# =====================================

uploaded_file = st.file_uploader(
    "Escolha um CSV",
    type=["csv"]
)

# =====================================
# PROCESSAMENTO
# =====================================

if uploaded_file is not None:

    try:

        # =============================
        # LEITURA CSV
        # =============================

        df = pd.read_csv(uploaded_file)

        # =============================
        # DETECTAR DATAS
        # =============================

        df, colunas_data = detectar_datas(df)

        if not colunas_data:

            st.warning(
                "Nenhuma coluna de data encontrada."
            )

        else:

            st.success(
                "Colunas de data detectadas!"
            )

            # =========================
            # SIDEBAR
            # =========================

            st.sidebar.header(
                "⚙️ Configurações"
            )

            coluna_data = st.sidebar.selectbox(
                "Coluna de Data",
                colunas_data
            )

            periodo = st.sidebar.selectbox(
                "Agrupar por",
                [
                    "Hora",
                    "Dia",
                    "Semana",
                    "Mês"
                ]
            )

            # =========================
            # COLUNAS NUMÉRICAS
            # =========================

            colunas_numericas = df.select_dtypes(
                include=["int64", "float64"]
            ).columns.tolist()

            coluna_valor = st.sidebar.selectbox(
                "Coluna Numérica",
                [None] + colunas_numericas
            )

            # =========================
            # AGRUPAMENTO
            # =========================

            df_agrupado = agrupar_periodo(
                df,
                coluna_data,
                periodo,
                coluna_valor
            )

            # =========================
            # KPIs
            # =========================

            st.subheader("📌 Indicadores")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Registros",
                    df.shape[0]
                )

            with col2:
                st.metric(
                    "Períodos",
                    df_agrupado.shape[0]
                )

            with col3:
                st.metric(
                    "Coluna Temporal",
                    coluna_data
                )

            st.divider()

            # =========================
            # GRÁFICO LINHA
            # =========================

            st.subheader(
                "📈 Evolução Temporal"
            )

            eixo_y = (
                coluna_valor
                if coluna_valor
                else 0
            )

            fig = px.line(
                df_agrupado,
                x=coluna_data,
                y=eixo_y,
                markers=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            # =========================
            # TABELA
            # =========================

            st.subheader("📄 Dados Agrupados")

            st.dataframe(
                df_agrupado,
                use_container_width=True
            )

    except Exception as e:

        st.error(f"Erro: {e}")