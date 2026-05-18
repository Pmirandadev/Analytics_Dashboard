import pandas as pd


def limpar_dados(df):

    # Remove duplicados
    df = df.drop_duplicates()

    # Remove espaços em branco
    df.columns = df.columns.str.strip()

    # Remove espaços em colunas texto
    for coluna in df.select_dtypes(include="object"):

        df[coluna] = df[coluna].astype(str).str.strip()

    return df


def relatorio_qualidade(df):

    relatorio = pd.DataFrame({
        "Coluna": df.columns,
        "Tipo": df.dtypes.values,
        "Valores Nulos": df.isnull().sum().values,
        "Valores Únicos": df.nunique().values
    })

    return relatorio