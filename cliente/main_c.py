# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    # Este ficheiro é o ponto de arranque do cliente , é onde o programa arranca e é onde se monta a zona para o user escrever os comandos no terminal
# -----------------------------

from cliente.processador_c import Processador
import sys
from sys import argv
from  shared.socket_utilities import PontoAcesso
from shared.excepcoes import ExcepcaoBase


def main():
    if len(argv) != 3:
        print("CLIENTE> Uso: python -m cliente.main <ip_zookeeper> <porto_zookeeper>")        
        sys.exit(1)

    ip_zookeeper = sys.argv[1]
    porto_zookeeper = sys.argv[2]
    hosts_zk = f"{ip_zookeeper}:{porto_zookeeper}"

    print("=========================================")
    print("        SEJA BEM-VINDO AO MARKETPLACE       ")
    print("=========================================")

    print("Perfis disponíveis:")
    print("  0 - Cliente Anónimo (Apenas para criar conta)")
    print("  1 - Cliente Registado (Para fazer compras)")
    print("  2 - Funcionário")
    print("  3 - Administrador (Para gerir loja)")
    print("-----------------------------------------")
    
    try:
        id_perfil = int(input("Introduz o teu Perfil (0-3): "))
        id_user = int(input("Introduz o teu ID de Utilizador: "))
    except ValueError:
        print("CLIENTE> Erro: O Perfil e o ID têm de ser números inteiros!")
        sys.exit(1)
        
    print(f"CLIENTE> A iniciar e a ligar ao ZooKeeper em {hosts_zk}...")


    # TODO: chama funcoes no cliente para contactar o servidor e enviar mensagensenviar_mensagem

    processador = Processador(hosts_zk, id_perfil, id_user)


    while True:
        
        pedido_user = input("Mensagem: ")
        
        if not pedido_user.strip():
            continue

        if pedido_user.strip().lower() in ['exit', 'quit']:
            processador.fechar_ligacao()
            print("CLIENTE> A encerrar...")
            break

        try:
            
            resultado = processador.processa(pedido_user)

            if resultado:
                print(resultado)

        except ExcepcaoBase as e:
            print(f"Erro: {e.msg}")

        except Exception as e:
            print(f"Erro inesperado: {e}")

if __name__ == '__main__':
    main()
