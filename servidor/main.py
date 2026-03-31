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

    porto_servidor = 8888

    if len(sys.argv) == 2:
        porto_servidor = int(sys.argv[1])
    elif len(sys.argv) > 2:
        print("SERVIDOR> Uso: python -m servidor.main [porto]")
        sys.exit(1)

    try:
        ponto_acesso = PontoAcesso(endereco_ip='127.0.0.1', porto=porto_servidor)  
        print("SERVIDOR> Configuracao do servidor válida.")

    except ExcepcaoConfiguracaoInvalida as e:
        print("SERVIDOR>", e.msg)
        sys.exit(1)

    skeleton = Skeleton(ponto_acesso)

    print(f"SERVIDOR> Servidor pronto em {ponto_acesso.endereco_ip}:{porto_servidor}")
    
    skeleton.iniciar_servidor()    

if __name__ == "__main__":
    main()