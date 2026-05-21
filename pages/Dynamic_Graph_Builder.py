import streamlit as st
import pandas as pd

from utils.graficos import criar_grafico

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="Dynamic Graph Builder",
    page_icon="🎨",
    layout="wide"
)

# =====================================
# TÍTULO
# =====================================

st.title("🎨 Dynamic Graph Builder")

st.write(
    "Crie gráficos dinamicamente com qualquer dataset."
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

        df = pd.read_csv(uploaded_file)

        st.success("Dataset carregado!")

        # =================================
        # TIPOS DE COLUNAS
        # =================================

        colunas = df.columns.tolist()

        colunas_numericas = df.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        # =================================
        # SIDEBAR
        # =================================

        st.sidebar.header("⚙️ Configurações")

        tipo_grafico = st.sidebar.selectbox(
            "Tipo de Gráfico",
            [
                "Barra",
                "Linha",
                "Pizza",
                "Scatter",
                "Histograma",
                "Boxplot"
            ]
        )

        eixo_x = st.sidebar.selectbox(
            "Eixo X",
            colunas
        )

        # =================================
        # EIXO Y
        # =================================

        if tipo_grafico in [
            "Barra",
            "Linha",
            "Scatter",
            "Boxplot",
            "Pizza"
        ]:

            eixo_y = st.sidebar.selectbox(
                "Eixo Y",
                colunas_numericas
            )

        else:

            eixo_y = None

        # =================================
        # COR
        # =================================

        cor = st.sidebar.selectbox(
            "Cor / Categoria",
            [None] + colunas
        )

        # =================================
        # AGREGAÇÃO
        # =================================

        agregacao = st.sidebar.selectbox(
            "Agregação",
            [
                "sum",
                "mean",
                "count",
                "max",
                "min"
            ]
        )

        # =================================
        # AGRUPAMENTO
        # =================================

        if eixo_y is not None:

            df_agrupado = df.groupby(
                eixo_x
            )[eixo_y]

            # Aplicando agregação
            if agregacao == "sum":
                df_agrupado = df_agrupado.sum()

            elif agregacao == "mean":
                df_agrupado = df_agrupado.mean()

            elif agregacao == "count":
                df_agrupado = df_agrupado.count()

            elif agregacao == "max":
                df_agrupado = df_agrupado.max()

            elif agregacao == "min":
                df_agrupado = df_agrupado.min()

            df_final = df_agrupado.reset_index()

        else:

            df_final = df

        # =================================
        # GRÁFICO
        # =================================

        fig = criar_grafico(
            df_final,
            tipo_grafico,
            eixo_x,
            eixo_y,
            cor
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =================================
        # DADOS
        # =================================

        st.subheader("📄 Dados Utilizados")

        st.dataframe(
            df_final,
            use_container_width=True
        )

        # =================================
        # DOWNLOAD
        # =================================

        csv = df_final.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Dados",
            csv,
            "dados_grafico.csv",
            "text/csv"
        )

    except Exception as e:

        st.error(f"Erro: {e}")