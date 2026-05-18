import pandas as pd


def realizar_merge(
    df1,
    df2,
    coluna_df1,
    coluna_df2,
    tipo_merge
):

    merged = pd.merge(
        df1,
        df2,
        left_on=coluna_df1,
        right_on=coluna_df2,
        how=tipo_merge
    )

    return merged