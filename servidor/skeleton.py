# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    # Este ficheiro é o Skeleton. Funciona como a "cozinha" do servidor. 
    # Recebe os pedidos em bytes da rede, traduz (pickle), manda para o processador, e empacota a resposta.
# -----------------------------

from servidor.rede import TCPSocketServidor
from servidor.loja import Loja
from servidor.processador import Processador
import pickle

class Skeleton:

    def __init__(self, ponto_acesso):
        self.rede = TCPSocketServidor(ponto_acesso)
        self.loja = Loja()
        self.processador = Processador(self)

    def iniciar_servidor(self):
        print("SERVIDOR> A iniciar serviços...")
        self.rede.aceitar(self.processa_pedido)

    def processa_pedido(self, pedido_bytes):
        try:
            pedido_em_lista = pickle.loads(pedido_bytes)
            
            resposta_em_lista = self.processador.processa(pedido_em_lista)

            resposta_bytes = pickle.dumps(resposta_em_lista)
            
            return resposta_bytes
            
        except Exception as e:
            print(f"SERVIDOR> Erro ao processar pedido no Skeleton: {e}")
            return pickle.dumps([39928, [str(e)]])


    def get_loja(self):
        return self.loja




        