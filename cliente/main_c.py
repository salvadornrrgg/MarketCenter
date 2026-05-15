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
    if len(argv) != 5:
        print("CLIENTE> Uso: python -m cliente.main <ip_zookeeper> <porto_zookeeper> <id_perfil> <id_utilizador>")        
        sys.exit(1)

    ip_zookeeper = sys.argv[1]
    porto_zookeeper = sys.argv[2]
    id_perfil = int(sys.argv[3])
    id_user = int(sys.argv[4])

    hosts_zk = f"{ip_zookeeper}:{porto_zookeeper}"
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
