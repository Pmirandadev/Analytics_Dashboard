import streamlit as st
import pandas as pd

from utils.merge import realizar_merge

# =====================================
# CONFIGURAÇÃO
# =====================================

st.set_page_config(
    page_title="Merge Datasets",
    page_icon="🔗",
    layout="wide"
)

# =====================================
# TÍTULO
# =====================================

st.title("🔗 Merge de Datasets")

st.write(
    "Faça upload de dois arquivos CSV e "
    "combine os datasets dinamicamente."
)

# =====================================
# UPLOAD DATASET 1
# =====================================

st.subheader("📁 Dataset 1")

file1 = st.file_uploader(
    "Upload CSV 1",
    type=["csv"],
    key="csv1"
)

# =====================================
# UPLOAD DATASET 2
# =====================================

st.subheader("📁 Dataset 2")

file2 = st.file_uploader(
    "Upload CSV 2",
    type=["csv"],
    key="csv2"
)

# =====================================
# PROCESSAMENTO
# =====================================

if file1 and file2:

    try:

        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        st.success("Datasets carregados!")

        # =================================
        # ESCOLHA COLUNAS
        # =================================

        col1, col2 = st.columns(2)

        with col1:

            coluna_df1 = st.selectbox(
                "Coluna Dataset 1",
                df1.columns
            )

        with col2:

            coluna_df2 = st.selectbox(
                "Coluna Dataset 2",
                df2.columns
            )

        # =================================
        # TIPO MERGE
        # =================================

        tipo_merge = st.selectbox(
            "Tipo de Merge",
            [
                "inner",
                "left",
                "right",
                "outer"
            ]
        )

        # =================================
        # BOTÃO
        # =================================

        if st.button("🚀 Realizar Merge"):

            merged = realizar_merge(
                df1,
                df2,
                coluna_df1,
                coluna_df2,
                tipo_merge
            )

            st.success("Merge realizado!")

            # =============================
            # MÉTRICAS
            # =============================

            colm1, colm2, colm3 = st.columns(3)

            with colm1:
                st.metric(
                    "Linhas",
                    merged.shape[0]
                )

            with colm2:
                st.metric(
                    "Colunas",
                    merged.shape[1]
                )

            with colm3:
                st.metric(
                    "Nulos",
                    merged.isnull().sum().sum()
                )

            st.divider()

            # =============================
            # TABELA
            # =============================

            st.subheader("📄 Dataset Final")

            st.dataframe(
                merged,
                use_container_width=True
            )

            # =============================
            # DOWNLOAD
            # =============================

            csv = merged.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "⬇️ Download CSV Final",
                csv,
                "dataset_merge.csv",
                "text/csv"
            )

    except Exception as e:

        st.error(f"Erro: {e}")