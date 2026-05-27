import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# CONFIG
# ======================================

st.set_page_config(
    page_title="Time Series Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Time Series Analytics")

st.write(
    "Análise temporal dos atendimentos."
)

# ======================================
# UPLOAD
# ======================================

uploaded_file = st.file_uploader(
    "Escolha um CSV tratado",
    type=["csv"]
)

# ======================================
# PROCESSAMENTO
# ======================================

if uploaded_file is not None:

    try:

        # ======================================
        # LEITURA
        # ======================================

        df = pd.read_csv(uploaded_file)

        # ======================================
        # CONVERSÕES
        # ======================================

        df["Data"] = pd.to_datetime(
            df["Data"]
        )

        df["Iniciado em"] = pd.to_datetime(
            df["Iniciado em"],
            format="%d/%m/%Y, %H:%M",
            errors="coerce",
            dayfirst=True
        )

        df["Finalizado em"] = pd.to_datetime(
            df["Finalizado em"],
            format="%d/%m/%Y, %H:%M",
            errors="coerce",
            dayfirst=True
        )

        df["Tempo de resposta"] = pd.to_timedelta(
            df["Tempo de resposta"]
        )

        df["Duração"] = pd.to_timedelta(
            df["Duração"]
        )

        # ======================================
        # COLUNAS AUXILIARES
        # ======================================

        df["Hora"] = (
            df["Iniciado em"]
            .dt.hour
        )

        df["Dia"] = (
            df["Data"]
            .dt.date
        )

        # ======================================
        # KPIs
        # ======================================

        total_atendimentos = df.shape[0]

        tma_medio = (
            df["Duração"]
            .mean()
        )

        resposta_media = (
            df["Tempo de resposta"]
            .mean()
        )

        chats_finalizados = (
            df["Finalizado em"]
            .notna()
            .sum()
        )

        # ======================================
        # KPIs VISUAIS
        # ======================================

        st.subheader("📌 Indicadores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Atendimentos",
                total_atendimentos
            )

        with col2:
            st.metric(
                "TMA Médio",
                str(tma_medio).split(".")[0]
            )

        with col3:
            st.metric(
                "Tempo Médio Resposta",
                str(resposta_media).split(".")[0]
            )

        with col4:
            st.metric(
                "Chats Finalizados",
                chats_finalizados
            )

        st.divider()

        # ======================================
        # ATENDIMENTOS POR DIA
        # ======================================

        atendimentos_dia = (
            df.groupby("Dia")
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
            use_container_width=True
        )

        # ======================================
        # TMA MÉDIO POR DIA
        # ======================================

        tma_dia = (
            df.groupby("Dia")["Duração"]
            .mean()
            .reset_index()
        )

        tma_dia["Duração"] = (
            tma_dia["Duração"]
            .astype(str)
            .str.split(".")
            .str[0]
        )

        fig_tma = px.bar(
            tma_dia,
            x="Dia",
            y="Duração",
            title="TMA Médio por Dia"
        )

        st.plotly_chart(
            fig_tma,
            use_container_width=True
        )

        # ======================================
        # TEMPO MÉDIO RESPOSTA
        # ======================================

        resposta_dia = (
            df.groupby("Dia")["Tempo de resposta"]
            .mean()
            .reset_index()
        )

        resposta_dia["Tempo de resposta"] = (
            resposta_dia["Tempo de resposta"]
            .astype(str)
            .str.split(".")
            .str[0]
        )

        fig_resposta = px.line(
            resposta_dia,
            x="Dia",
            y="Tempo de resposta",
            markers=True,
            title="Tempo Médio de Resposta"
        )

        st.plotly_chart(
            fig_resposta,
            use_container_width=True
        )

        # ======================================
        # HEATMAP
        # ======================================

        heatmap = (
            df.groupby(["Dia", "Hora"])
            .size()
            .reset_index(name="Atendimentos")
        )

        fig_heatmap = px.density_heatmap(
            heatmap,
            x="Hora",
            y="Dia",
            z="Atendimentos",
            title="HeatMap Atendimentos por Hora"
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )

        # ======================================
        # TABELA ANALÍTICA
        # ======================================

        st.subheader("📄 Dataset Analítico")

        st.dataframe(
            df,
            use_container_width=True
        )

    except Exception as e:

        st.error(f"Erro: {e}")