import pandas as pd


def detectar_datas(df):

    colunas_data = []

    for coluna in df.columns:

        try:

            df[coluna] = pd.to_datetime(
                df[coluna]
            )

            colunas_data.append(coluna)

        except:

            pass

    return df, colunas_data


def agrupar_periodo(
    df,
    coluna_data,
    periodo,
    coluna_valor=None
):

    df = df.copy()

    # Define índice temporal
    df[coluna_data] = pd.to_datetime(
        df[coluna_data]
    )

    df = df.set_index(coluna_data)

    # ============================
    # AGRUPAMENTO
    # ============================

    if periodo == "Dia":
        regra = "D"

    elif periodo == "Semana":
        regra = "W"

    elif periodo == "Mês":
        regra = "M"

    elif periodo == "Hora":
        regra = "H"

    # ============================
    # AGREGAÇÃO
    # ============================

    if coluna_valor:

        agrupado = df[
            coluna_valor
        ].resample(regra).sum()

    else:

        agrupado = df.resample(
            regra
        ).size()

    return agrupado.reset_index()