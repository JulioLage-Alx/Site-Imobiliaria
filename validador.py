import re
from datetime import datetime

def validar_cep(cep):
    return bool(re.fullmatch(r'\d{5}-\d{3}', cep))

def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:
        return False
    def calcular_dv(cpf, pesos):
        total = sum(int(cpf[i]) * pesos[i] for i in range(len(pesos)))
        resto = total % 11
        return 0 if resto < 2 else 11 - resto
    pesos1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    dv1 = calcular_dv(cpf, pesos1)
    dv2 = calcular_dv(cpf, pesos2)
    return cpf[-2:] == f"{dv1}{dv2}"

def validar_telefone(telefone):
    return bool(re.fullmatch(r'\d{2}[9]?\d{8}', telefone))

def validar_valor(valor):
    try:
        valor = float(valor)
        return valor > 1
    except ValueError:
        return False

def validar_data(data):
    try:
        data_nascimento = datetime.strptime(data, "%Y-%m-%d")
        return data_nascimento < datetime.today()
    except ValueError:
        return False
