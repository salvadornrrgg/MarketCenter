import re
from shared.excepcoes import TipoArgumentoInvalido
#---------------------------
# Normaliza comando textual
#---------------------------

def normalizar_nome(nome): 
    if type(nome) is not str:
        raise TipoArgumentoInvalido("nome")
    # remove espaços extremos
    nome = nome.strip()

    nome = nome.replace('"', '').replace("'", '')

    # substitui múltiplos espaços por 1 só
    nome = re.sub(r'\s+', ' ', nome)

    # normaliza capitalização
    return nome.lower().title()