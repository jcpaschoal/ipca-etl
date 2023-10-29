import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd
import os


import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd
import os


def generate_report(user_xls, log_xls, output_pdf):
    users_df = pd.read_excel(user_xls)
    logs_df = pd.read_excel(log_xls)
    merged_df = pd.merge(users_df, logs_df, on="cpf")

    images = []

    users_df["idade"].hist(bins=20, edgecolor="k", alpha=0.75)
    plt.title("Distribuição das Idades dos Usuários")
    plt.xlabel("Idade")
    plt.ylabel("Número de Usuários")
    plt.tight_layout()
    img_name = "age_distribution.png"
    plt.savefig(img_name, dpi=300)
    images.append(img_name)
    plt.clf()

    mean_values = merged_df.groupby("tipo_conta")["valor_da_movimentacao"].mean()
    mean_values.plot(kind="bar", color="skyblue", edgecolor="k", alpha=0.75)
    plt.title("Valor Médio da Movimentação por Tipo de Conta")
    plt.ylabel("Valor Médio (R$)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    img_name = "avg_transaction_per_account.png"
    plt.savefig(img_name, dpi=300)
    images.append(img_name)
    plt.clf()

    users_per_account_type = users_df["tipo_conta"].value_counts()
    users_per_account_type.plot(kind="bar", color="green", edgecolor="k", alpha=0.75)
    plt.title("Número de Usuários por Tipo de Conta")
    plt.ylabel("Número de Usuários")
    plt.xticks(rotation=0)
    plt.tight_layout()
    img_name = "users_per_account_type.png"
    plt.savefig(img_name, dpi=300)
    images.append(img_name)
    plt.clf()

    avg_transactions = merged_df.groupby("tipo_conta").size()
    avg_transactions.plot(kind="bar", color="limegreen", edgecolor="k", alpha=0.75)
    plt.title("Média de Transações por Tipo de Conta")
    plt.ylabel("Número Médio de Transações")
    plt.xticks(rotation=0)
    plt.tight_layout()
    img_name = "avg_transactions_per_account_type.png"
    plt.savefig(img_name, dpi=300)
    images.append(img_name)
    plt.clf()

    professions = (
        merged_df.groupby("profissao")["valor_da_movimentacao"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    professions.plot(kind="barh", color="lightsalmon", edgecolor="k", alpha=0.75)
    plt.title("Top 10 Profissões com Maior Valor Médio de Movimentação")
    plt.xlabel("Valor Médio (R$)")
    plt.tight_layout()
    img_name = "top_professions_by_value.png"
    plt.savefig(img_name, dpi=300)
    images.append(img_name)
    plt.clf()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)

    for image in images:
        pdf.add_page()
        pdf.cell(200, 10, "Relatório de Insights de Usuários e Transações", 0, 1, "C")
        pdf.image(image, x=10, y=pdf.get_y(), w=190)

    pdf.output(output_pdf)

    for image in images:
        os.remove(image)
