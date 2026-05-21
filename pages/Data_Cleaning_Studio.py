import streamlit as st
import pandas as pd

from utils.cleaning import (
    remover_colunas,
    remover_nulos,
    preencher_nulos,
    remover_duplicados,
    normalizar_texto,
    converter_tipo,
    renomear_coluna,
    remover_caracteres,
    detectar_outliers
)

# ===================================
# CONFIG
# ===================================

st.set_page_config(
    page_title="Data Cleaning Studio",
    page_icon="🧹",
    layout="wide"
)

# ===================================
# TÍTULO
# ===================================

st.title("🧹 Data Cleaning Studio")

st.write(
    "Limpeza e tratamento interativo de datasets."
)

# ===================================
# UPLOAD
# ===================================

uploaded_file = st.file_uploader(
    "Escolha um CSV",
    type=["csv"]
)

# ===================================
# PROCESSAMENTO
# ===================================

if uploaded_file is not None:

    try:

        # ==============================
        # LEITURA CSV
        # ==============================

        df = pd.read_csv(uploaded_file)

        st.success("Dataset carregado!")

        # ==============================
        # CÓPIA DATAFRAME
        # ==============================

        df_tratado = df.copy()

        # ==============================
        # SIDEBAR
        # ==============================

        st.sidebar.header("⚙️ Transformações")

        # ===================================
        # REMOVER COLUNAS
        # ===================================

        st.sidebar.subheader("🗑️ Remover Colunas")

        colunas_remover = st.sidebar.multiselect(
            "Selecionar Colunas",
            df_tratado.columns.tolist()
        )

        if colunas_remover:

            df_tratado = remover_colunas(
                df_tratado,
                colunas_remover
            )

        # ===================================
        # REMOVER NULOS
        # ===================================

        st.sidebar.subheader("❌ Valores Nulos")

        remover_null = st.sidebar.checkbox(
            "Remover linhas com nulos"
        )

        if remover_null:

            df_tratado = remover_nulos(
                df_tratado
            )

        # ===================================
        # PREENCHER NULOS
        # ===================================

        preencher = st.sidebar.selectbox(
            "Preencher Nulos",
            [
                "Nenhum",
                "Média",
                "Mediana",
                "Zero"
            ]
        )

        if preencher != "Nenhum":

            df_tratado = preencher_nulos(
                df_tratado,
                preencher
            )

        # ===================================
        # REMOVER DUPLICADOS
        # ===================================

        st.sidebar.subheader("📄 Duplicados")

        duplicados = st.sidebar.checkbox(
            "Remover Duplicados"
        )

        if duplicados:

            df_tratado = remover_duplicados(
                df_tratado
            )

        # ===================================
        # NORMALIZAR TEXTO
        # ===================================

        st.sidebar.subheader("🔤 Texto")

        normalizar = st.sidebar.checkbox(
            "Normalizar Texto"
        )

        if normalizar:

            df_tratado = normalizar_texto(
                df_tratado
            )

        # ===================================
        # RENOMEAR COLUNAS
        # ===================================

        st.sidebar.subheader("✏️ Renomear Colunas")

        coluna_rename = st.sidebar.selectbox(
            "Selecionar Coluna",
            [None] + df_tratado.columns.tolist(),
            key="rename_coluna"
        )

        if coluna_rename:

            novo_nome = st.sidebar.text_input(
                "Novo Nome"
            )

            if novo_nome:

                df_tratado = renomear_coluna(
                    df_tratado,
                    coluna_rename,
                    novo_nome
                )

        # ===================================
        # CONVERTER TIPOS
        # ===================================

        st.sidebar.subheader("🔄 Converter Tipos")

        coluna_tipo = st.sidebar.selectbox(
            "Coluna para Conversão",
            [None] + df_tratado.columns.tolist(),
            key="converter_tipo"
        )

        if coluna_tipo:

            tipo = st.sidebar.selectbox(
                "Novo Tipo",
                [
                    "string",
                    "int",
                    "float",
                    "datetime"
                ]
            )

            df_tratado = converter_tipo(
                df_tratado,
                coluna_tipo,
                tipo
            )

        # ===================================
        # REMOVER CARACTERES
        # ===================================

        st.sidebar.subheader("🧽 Remover Caracteres")

        coluna_char = st.sidebar.selectbox(
            "Coluna Texto",
            [None] + df_tratado.columns.tolist(),
            key="remover_char"
        )

        if coluna_char:

            caracteres = st.sidebar.text_input(
                "Caracteres ou Regex"
            )

            if caracteres:

                df_tratado = remover_caracteres(
                    df_tratado,
                    coluna_char,
                    caracteres
                )

        # ===================================
        # DETECTAR OUTLIERS
        # ===================================

        st.sidebar.subheader("🚨 Detectar Outliers")

        colunas_numericas = df_tratado.select_dtypes(
            include=["int64", "float64", "Int64"]
        ).columns.tolist()

        coluna_outlier = st.sidebar.selectbox(
            "Coluna Numérica",
            [None] + colunas_numericas
        )

        outliers = pd.DataFrame()

        if coluna_outlier:

            outliers = detectar_outliers(
                df_tratado,
                coluna_outlier
            )

        # ===================================
        # KPIs
        # ===================================

        st.subheader("📌 Indicadores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Linhas Originais",
                df.shape[0]
            )

        with col2:
            st.metric(
                "Linhas Tratadas",
                df_tratado.shape[0]
            )

        with col3:
            st.metric(
                "Colunas",
                df_tratado.shape[1]
            )

        with col4:
            st.metric(
                "Outliers",
                outliers.shape[0]
            )

        st.divider()

        # ===================================
        # DATASETS
        # ===================================

        col_original, col_tratado = st.columns(2)

        with col_original:

            st.subheader("📄 Dataset Original")

            st.dataframe(
                df,
                use_container_width=True
            )

        with col_tratado:

            st.subheader("🧹 Dataset Tratado")

            st.dataframe(
                df_tratado,
                use_container_width=True
            )

        # ===================================
        # OUTLIERS
        # ===================================

        if not outliers.empty:

            st.divider()

            st.subheader(
                f"🚨 Outliers Detectados em '{coluna_outlier}'"
            )

            st.dataframe(
                outliers,
                use_container_width=True
            )

        # ===================================
        # DOWNLOAD
        # ===================================

        st.divider()

        csv = df_tratado.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Dataset Tratado",
            csv,
            "dataset_tratado.csv",
            "text/csv"
        )

    except Exception as e:

        st.error(f"Erro: {e}")