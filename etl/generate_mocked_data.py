import csv
import random
from faker import Faker
import os


faker = Faker("pt_BR")


def generate_user_data(num_users):
    data = []
    for _ in range(num_users):
        cpf = faker.unique.cpf()
        primeiro_nome = faker.first_name()
        ultimo_nome = faker.last_name()
        email = faker.email()
        rua = faker.street_name()
        cep = faker.postcode()
        cidade = faker.city()
        idade = random.randint(18, 75)
        estado_civil = random.choice([None, "solteiro", "casado", "divorciado"])
        profissao = random.choice(
            [None, "engenheiro", "medico", "professor", "advogado"]
        )
        tipo_conta = random.choice(["basica", "plus", "premium"])

        # Variando entre uppercase, lowercase e capitalize
        primeiro_nome = random.choice(
            [primeiro_nome.upper(), primeiro_nome.lower(), primeiro_nome.capitalize()]
        )
        ultimo_nome = random.choice(
            [ultimo_nome.upper(), ultimo_nome.lower(), ultimo_nome.capitalize()]
        )
        if estado_civil:
            estado_civil = random.choice(
                [estado_civil.upper(), estado_civil.lower(), estado_civil.capitalize()]
            )
        if profissao:
            profissao = random.choice(
                [profissao.upper(), profissao.lower(), profissao.capitalize()]
            )

        data.append(
            [
                cpf,
                primeiro_nome,
                ultimo_nome,
                email,
                rua,
                cep,
                cidade,
                idade,
                estado_civil,
                profissao,
                tipo_conta,
            ]
        )

    return data


def generate_log_data(users, num_logs):
    data = []
    for _ in range(num_logs):
        user = random.choice(users)
        cpf = user[0]
        tipo_conta = user[10]

        if tipo_conta == "basica":
            saldo_antes = random.uniform(100, 5000)
            valor_movimentacao = random.uniform(1, 1000)
        elif tipo_conta == "plus":
            saldo_antes = random.uniform(2000, 8000)
            valor_movimentacao = random.uniform(1, 2000)
        elif tipo_conta == "premium":
            saldo_antes = random.uniform(3000, 25000)
            valor_movimentacao = random.uniform(2, 10000)

        saldo_depois = (
            saldo_antes - valor_movimentacao
            if valor_movimentacao <= saldo_antes
            else saldo_antes
        )
        status = "completed" if valor_movimentacao <= saldo_antes else "denied"
        motivo_movimentacao = random.choice(
            [None, "pagamento", "transferencia", "saque", "deposito"]
        )
        horario_movimentacao = faker.date_time_this_year()

        data.append(
            [
                cpf,
                saldo_antes,
                saldo_depois,
                valor_movimentacao,
                status,
                motivo_movimentacao,
                horario_movimentacao,
            ]
        )

    return data


def save_user_to_csv(data, filename, path="."):
    full_path = os.path.join(path, filename)
    with open(full_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "cpf",
                "primeiro_nome",
                "ultimo_nome",
                "email",
                "rua",
                "cep",
                "cidade",
                "idade",
                "estado_civil",
                "profissao",
                "tipo_conta",
            ]
        )
        writer.writerows(data)


def save_log_to_csv(data, filename, path="."):
    full_path = os.path.join(path, filename)
    with open(full_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "cpf",
                "saldo_antes_da_operacao",
                "saldo_depois_da_operacao",
                "valor_da_movimentacao",
                "status",
                "motivo_da_movimentacao",
                "horario_movimentacao",
            ]
        )
        writer.writerows(data)
