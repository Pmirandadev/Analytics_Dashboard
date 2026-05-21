import pandas as pd


# ==============================
# REMOVER COLUNAS
# ==============================

def remover_colunas(df, colunas):

    return df.drop(columns=colunas)


# ==============================
# REMOVER NULOS
# ==============================

def remover_nulos(df):

    return df.dropna()


# ==============================
# PREENCHER NULOS
# ==============================

def preencher_nulos(df, metodo):

    df = df.copy()

    colunas_numericas = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for coluna in colunas_numericas:

        if metodo == "Média":

            df[coluna] = df[coluna].fillna(
                df[coluna].mean()
            )

        elif metodo == "Mediana":

            df[coluna] = df[coluna].fillna(
                df[coluna].median()
            )

        elif metodo == "Zero":

            df[coluna] = df[coluna].fillna(0)

    return df


# ==============================
# REMOVER DUPLICADOS
# ==============================

def remover_duplicados(df):

    return df.drop_duplicates()


# ==============================
# NORMALIZAR TEXTO
# ==============================

def normalizar_texto(df):

    df = df.copy()

    colunas_texto = df.select_dtypes(
        include="object"
    ).columns

    for coluna in colunas_texto:

        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    return df

# ==============================
# CONVERTER TIPOS
# ==============================

def converter_tipo(df, coluna, tipo):

    df = df.copy()

    try:

        if tipo == "string":

            df[coluna] = df[coluna].astype(str)

        elif tipo == "int":

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            ).astype("Int64")

        elif tipo == "float":

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )

        elif tipo == "datetime":

            df[coluna] = pd.to_datetime(
                df[coluna],
                errors="coerce"
            )

    except:

        pass

    return df


# ==============================
# RENOMEAR COLUNAS
# ==============================

def renomear_coluna(df, coluna_antiga, coluna_nova):

    return df.rename(
        columns={
            coluna_antiga: coluna_nova
        }
    )


# ==============================
# REMOVER CARACTERES
# ==============================

def remover_caracteres(
    df,
    coluna,
    caracteres
):

    df = df.copy()

    df[coluna] = (
        df[coluna]
        .astype(str)
        .str.replace(
            caracteres,
            "",
            regex=True
        )
    )

    return df


# ==============================
# DETECTAR OUTLIERS
# ==============================

def detectar_outliers(df, coluna):

    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)

    IQR = Q3 - Q1

    inferior = Q1 - 1.5 * IQR
    superior = Q3 + 1.5 * IQR

    outliers = df[
        (df[coluna] < inferior)
        | (df[coluna] > superior)
    ]

    return outliers