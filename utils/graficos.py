import plotly.express as px
import pandas as pd


def criar_grafico(
    df,
    tipo_grafico,
    eixo_x,
    eixo_y,
    cor=None
):

    # =========================
    # BARRAS
    # =========================

    if tipo_grafico == "Barra":

        fig = px.bar(
            df,
            x=eixo_x,
            y=eixo_y,
            color=cor,
            barmode="group"
        )

    # =========================
    # LINHA
    # =========================

    elif tipo_grafico == "Linha":

        fig = px.line(
            df,
            x=eixo_x,
            y=eixo_y,
            color=cor
        )

    # =========================
    # PIZZA
    # =========================

    elif tipo_grafico == "Pizza":

        fig = px.pie(
            df,
            names=eixo_x,
            values=eixo_y
        )

    # =========================
    # SCATTER
    # =========================

    elif tipo_grafico == "Scatter":

        fig = px.scatter(
            df,
            x=eixo_x,
            y=eixo_y,
            color=cor,
            size=eixo_y
        )

    # =========================
    # HISTOGRAMA
    # =========================

    elif tipo_grafico == "Histograma":

        fig = px.histogram(
            df,
            x=eixo_x,
            color=cor
        )

    # =========================
    # BOXPLOT
    # =========================

    elif tipo_grafico == "Boxplot":

        fig = px.box(
            df,
            x=eixo_x,
            y=eixo_y,
            color=cor
        )

    return fig