import re
from datetime import datetime

# Validação do CEP
def validar_cep(cep):
    return bool(re.fullmatch(r'\d{8}', cep))

# Validação do CPF (básica)
def validar_cpf(cpf):
    
    return len(cpf) == 11 and cpf.isdigit()


# Validação do telefone
def validar_telefone(telefone):
    return bool(re.fullmatch(r'\d{10,11}', telefone))

# Validação do valor do aluguel
def validar_valor(valor):
    try:
        return float(valor) > 0
    except ValueError:
        return False

# Validação da data de nascimento
def validar_data(data):
    try:
        datetime.strptime(data, "%Y-%m-%d")
        return True
    except ValueError:
        return False
