import pandas as pd

def preparar_dataset_temporal(df):

    # Remove colunas Unnamed
    df = df.loc[
        :,
        ~df.columns.str.contains("^Unnamed")
    ]

    colunas_data = []

    possiveis_datas = [
        "Data",
        "Iniciado em",
        "Respondido em",
        "Finalizado em"
    ]

    for coluna in possiveis_datas:

        if coluna in df.columns:

            try:

                # Coluna usada apenas para agrupamento diário
                if coluna == "Data":

                    df[coluna] = pd.to_datetime(
                        df[coluna],
                        errors="coerce",
                        dayfirst=True
                    ).dt.date

                # Colunas que precisam manter hora/minuto/segundo
                else:

                    df[coluna] = pd.to_datetime(
                        df[coluna],
                        errors="coerce",
                        dayfirst=True
                    )

                colunas_data.append(coluna)

            except Exception:
                pass

    return df, colunas_data

def agrupar_periodo(
    df,
    coluna_data,
    periodo,
    coluna_valor=None
    ):

    df = df.copy()

    df = df.set_index(coluna_data)

    regras = {
        "Hora": "h",
        "Dia": "D",
        "Semana": "W",
        "Mês": "MS"
    }

    regra = regras.get(periodo, "D")

    if coluna_valor:

        agrupado = (
            df[coluna_valor]
            .resample(regra)
            .mean()
        )

    else:

        agrupado = (
            df
            .resample(regra)
            .size()
        )

    return agrupado.reset_index()