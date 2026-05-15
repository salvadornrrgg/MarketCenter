# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Neste ficheiro é onde se arranca o servidor, ele fica `espera` que os clientes cheguem com os pedidos
# -----------------------------

import sys
from servidor.skeleton import Skeleton
from shared.excepcoes import ExcepcaoConfiguracaoInvalida
from shared.socket_utilities import PontoAcesso

def main():
    if len(sys.argv) != 4:
        print("SERVIDOR> Uso: python -m servidor.main <porto_servidor> <ip_zookeeper> <porto_zookeeper>")
        sys.exit(1)

    porto_servidor = int(sys.argv[1])
    ip_zookeeper = sys.argv[2]
    porto_zookeeper = sys.argv[3]
    
    hosts_zk = f"{ip_zookeeper}:{porto_zookeeper}"

    try:
        ponto_acesso = PontoAcesso(endereco_ip='0.0.0.0', porto=porto_servidor)  
        print("SERVIDOR> Configuracao do servidor válida.")

    except ExcepcaoConfiguracaoInvalida as e:
        print("SERVIDOR>", e.msg)
        sys.exit(1)

    skeleton = Skeleton(ponto_acesso, hosts_zk)

    print(f"SERVIDOR> Servidor pronto em {ponto_acesso.endereco_ip}:{porto_servidor}")
    print(f"SERVIDOR> A tentar ligar ao ZooKeeper em {hosts_zk}")
    
    skeleton.iniciar_servidor()    

if __name__ == "__main__":
    main()