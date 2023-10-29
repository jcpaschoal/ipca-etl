import pandas as pd

import os
import pandas as pd


def transform_users_csv(input_csv, output_xls, path="."):
    df = pd.read_csv(input_csv)
    df["primeiro_nome"] = df["primeiro_nome"].str.lower().str.strip ()
    df["ultimo_nome"] = df["ultimo_nome"].str.lower().str.strip()
    df["rua"] = df["rua"].str.lower().str.strip()
    if "estado_civil" in df:
        df["estado_civil"] = df["estado_civil"].str.lower().str.strip()
    if "profissao" in df:
        df["profissao"] = df["profissao"].str.lower().str.strip()
    df["cpf"] = df["cpf"].str.replace(".", "").str.replace("-", "")
    df["cep"] = df["cep"].str.replace("-", "")

    full_path = os.path.join(path, output_xls)
    df.to_excel(full_path, index=False)


def transform_logs_csv(input_csv, output_xls, path="."):
    df = pd.read_csv(input_csv)
    df = df[df["status"] != "denied"]
    df["cpf"] = df["cpf"].str.replace(".", "").str.replace("-", "")
    full_path = os.path.join(path, output_xls)
    df.to_excel(full_path, index=False)


import pandas as pd


def aggregate_user_logs(user_xls, log_xls, output_xls, path="."):
    user_df = pd.read_excel(os.path.join(path, user_xls), engine='openpyxl')
    log_df = pd.read_excel(os.path.join(path, log_xls), engine='openpyxl')

    merged_df = pd.merge(user_df, log_df, on="cpf", how="left")


    aggregated_df = merged_df.groupby("cpf").agg({
        "valor_da_movimentacao": ["sum", "count", "mean"],
        "saldo_antes_da_operacao": "mean",
        "saldo_depois_da_operacao": "mean",
    }).reset_index()

    aggregated_df.columns = ["_".join(col).strip() for col in aggregated_df.columns.values]

    aggregated_df.to_excel(os.path.join(path, output_xls), index=False)

