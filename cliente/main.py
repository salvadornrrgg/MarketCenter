# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    # Este ficheiro é o ponto de arranque do cliente , é onde o programa arranca e é onde se monta a zona para o user escrever os comandos no terminal
# -----------------------------



from cliente.stub import Stub
from sys import argv
import sys, shlex
from  shared.socket_utilities import PontoAcesso
from shared.excepcoes import ExcepcaoConfiguracaoInvalida


def main():
    if len(argv) != 2:
        print("CLIENTE> Uso: python -m cliente.main <porto>")
        sys.exit(1)

    try: 
        # valida endereco_ip e porto (se erro ExcepcaoIPInvalido ou ExcepcaoPortoInvalido)
        ponto_acesso = PontoAcesso(endereco_ip = 'localhost', porto = int(argv[1]))
        print("CLIENTE> Configuracao do servidor válida. ")
        print("CLIENTE> Iniciando aplicação do lado do cliente. ")
    except ExcepcaoConfiguracaoInvalida  as e: 
        print("CLIENTE>", e)
        sys.exit(1) 

    # TODO: chama funcoes no cliente para contactar o servidor e enviar mensagensenviar_mensagem

    id_perfil = int(input("Introduza o ID do Perfil (0=Anónimo, 1=Cliente, 2=Funcionario, 3=Admin):"))
    id_user = int(input("Introduza o ID do Utilizador:"))
    stub = Stub(ponto_acesso)

    codigos_operacoes = {
        "CRIA_CATEGORIA": 10100,
        "LISTA_CATEGORIAS": 10200,
        "REMOVE_CATEGORIA": 10300,
        "CRIA_PRODUTO": 10400,
    # ... adicionas os outros depois ...
    }

    while True:
        pedido_user = input("CLIENTE> Introduza o comando: ")
        if not pedido_user.strip():
            continue

        if pedido_user.strip().lower() in ['exit', 'quit']:
            stub.fechar_ligacao()
            print("CLIENTE> A encerrar...")
            break

        try:
            pedido_partido = shlex.split(pedido_user)
            if not pedido_partido:
                continue

            comando = pedido_partido[0].upper()
            argumentos = pedido_partido[1:]

            if comando not in codigos_operacoes:
                print(f"CLIENTE> Comando '{comando}' desconhecido.")
                continue

            op_code = codigos_operacoes[comando]

            pedido_em_lista = [op_code, argumentos, id_perfil, id_user]
            resposta = stub.processa(pedido_em_lista)
            print(f"SERVIDOR> {resposta}")

        except Exception as e:
            print(f"CLIENTE> Erro: {e}")

