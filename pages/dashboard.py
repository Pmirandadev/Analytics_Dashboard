import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# CONFIG
# ======================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================
# TÍTULO
# ======================================

st.title("📊 Dashboard Comparativo")

st.write(
    "Comparação consolidada entre datasets tratados."
)

# ======================================
# UPLOAD MÚLTIPLO
# ======================================

uploaded_files = st.file_uploader(
    "Escolha os CSVs tratados",
    type=["csv"],
    accept_multiple_files=True
)

# ======================================
# PROCESSAMENTO
# ======================================

if uploaded_files:

    try:

        lista_dfs = []

        # ======================================
        # COLUNAS OBRIGATÓRIAS
        # ======================================

        colunas_obrigatorias = [
            "Data",
            "Iniciado em",
            "Finalizado em",
            "Duração",
            "Tempo de resposta"
        ]

        # ======================================
        # LEITURA DOS CSVs
        # ======================================

        for file in uploaded_files:

            try:

                df = pd.read_csv(file)

                # ======================================
                # VALIDA COLUNAS
                # ======================================

                colunas_faltando = [
                    col
                    for col in colunas_obrigatorias
                    if col not in df.columns
                ]

                if colunas_faltando:

                    st.warning(
                        f"""
                        Arquivo '{file.name}'
                        ignorado.

                        Colunas faltando:
                        {colunas_faltando}
                        """
                    )

                    continue

                # ======================================
                # IDENTIFICAÇÃO
                # ======================================

                df["Arquivo"] = file.name

                # ======================================
                # PADRONIZAÇÃO DATAS
                # ======================================

                df["Data"] = pd.to_datetime(
                    df["Data"],
                    format="mixed",
                    errors="coerce",
                    dayfirst=True
                )

                df["Iniciado em"] = pd.to_datetime(
                    df["Iniciado em"],
                    format="mixed",
                    errors="coerce",
                    dayfirst=True
                )

                df["Finalizado em"] = pd.to_datetime(
                    df["Finalizado em"],
                    format="mixed",
                    errors="coerce",
                    dayfirst=True
                )

                # ======================================
                # TIMEDelta
                # ======================================

                df["Duração"] = pd.to_timedelta(
                    df["Duração"],
                    errors="coerce"
                )

                df["Tempo de resposta"] = pd.to_timedelta(
                    df["Tempo de resposta"],
                    errors="coerce"
                )

                # ======================================
                # REMOVE LINHAS INVÁLIDAS
                # ======================================

                df = df.dropna(
                    subset=[
                        "Data",
                        "Iniciado em"
                    ]
                )

                lista_dfs.append(df)

                st.success(
                    f"✔ {file.name} carregado"
                )

            except Exception as e:

                st.error(
                    f"""
                    Erro no arquivo:
                    {file.name}

                    {e}
                    """
                )

        # ======================================
        # VALIDA DATAFRAMES
        # ======================================

        if len(lista_dfs) == 0:

            st.stop()

        # ======================================
        # CONCATENAÇÃO
        # ======================================

        df_final = pd.concat(
            lista_dfs,
            ignore_index=True
        )

        # ======================================
        # COLUNAS AUXILIARES
        # ======================================

        df_final["Hora"] = (
            df_final["Iniciado em"]
            .dt.hour
        )

        df_final["Dia"] = (
            df_final["Data"]
            .dt.date
        )

        # ======================================
        # KPIs
        # ======================================

        total_atendimentos = (
            df_final.shape[0]
        )

        tma_geral = (
            df_final["Duração"]
            .mean()
        )

        resposta_media = (
            df_final["Tempo de resposta"]
            .mean()
        )

        chats_finalizados = (
            df_final["Finalizado em"]
            .notna()
            .sum()
        )

        quantidade_arquivos = (
            len(uploaded_files)
        )

        # ======================================
        # KPIs VISUAIS
        # ======================================

        st.subheader("📌 Indicadores")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Atendimentos",
                total_atendimentos
            )

        with col2:
            st.metric(
                "TMA Geral",
                str(tma_geral).split(".")[0]
            )

        with col3:
            st.metric(
                "Tempo Resposta",
                str(resposta_media).split(".")[0]
            )

        with col4:
            st.metric(
                "Chats Finalizados",
                chats_finalizados
            )

        with col5:
            st.metric(
                "Arquivos",
                quantidade_arquivos
            )

        st.divider()

        # ======================================
        # ATENDIMENTOS POR DIA
        # ======================================

        atendimentos_dia = (
            df_final.groupby("Dia")
            .size()
            .reset_index(name="Atendimentos")
        )

        fig_atendimentos = px.line(
            atendimentos_dia,
            x="Dia",
            y="Atendimentos",
            markers=True,
            title="Atendimentos por Dia"
        )

        st.plotly_chart(
            fig_atendimentos,
            use_container_width=True,
            key="dashboard_atendimentos"
        )

        # ======================================
        # COMPARAÇÃO ENTRE CSVs
        # ======================================

        comparacao_csv = (
            df_final.groupby("Arquivo")
            .size()
            .reset_index(name="Atendimentos")
        )

        fig_csv = px.bar(
            comparacao_csv,
            x="Arquivo",
            y="Atendimentos",
            text="Atendimentos",
            title="Comparação entre CSVs"
        )

        st.plotly_chart(
            fig_csv,
            use_container_width=True,
            key="dashboard_csv"
        )

        # ======================================
        # TMA POR CSV
        # ======================================

        tma_csv = (
            df_final.groupby("Arquivo")["Duração"]
            .mean()
            .reset_index()
        )

        tma_csv["Duracao_Horas"] = (
            tma_csv["Duração"]
            .dt.total_seconds() / 3600
        )

        tma_csv["Duracao_Formatada"] = (
            tma_csv["Duração"]
            .astype(str)
            .str.split(".")
            .str[0]
        )

        fig_tma = px.bar(
            tma_csv,
            x="Arquivo",
            y="Duracao_Horas",
            text="Duracao_Formatada",
            title="TMA Médio por Arquivo"
        )

        fig_tma.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig_tma,
            use_container_width=True,
            key="dashboard_tma"
        )

        # ======================================
        # HEATMAP
        # ======================================

        heatmap = (
            df_final.groupby(["Dia", "Hora"])
            .size()
            .reset_index(name="Atendimentos")
        )

        fig_heatmap = px.density_heatmap(
            heatmap,
            x="Hora",
            y="Dia",
            z="Atendimentos",
            title="HeatMap Consolidado"
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True,
            key="dashboard_heatmap"
        )

        # ======================================
        # DATASET
        # ======================================

        st.subheader("📄 Dataset Consolidado")

        st.dataframe(
            df_final,
            use_container_width=True
        )

        # ======================================
        # DOWNLOAD
        # ======================================

        csv = df_final.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download Dataset Consolidado",
            csv,
            "dataset_consolidado.csv",
            "text/csv"
        )

    except Exception as e:

        st.error(f"Erro: {e}")