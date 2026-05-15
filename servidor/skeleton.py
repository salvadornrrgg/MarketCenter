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
from servidor.zookeeperServidor import ZooKeeperServidor

class Skeleton:

    def __init__(self, ponto_acesso):
        self.rede = TCPSocketServidor(ponto_acesso)
        self.loja = Loja()
        self.processador = Processador(self)
        self.zookeeper = ZooKeeperServidor(ponto_acesso.porto)

    def iniciar_servidor(self):
        print("SERVIDOR> A iniciar serviços...")
        self.zookeeper.connect()
        self.rede.aceitar(self.processa_pedido)

    def processa_pedido(self, pedido_bytes):
        try:
            pedido_em_lista = pickle.loads(pedido_bytes)
        except Exception as e:
            print(f"SERVIDOR> Erro 39909: {e}")
            return pickle.dumps([39909, ["Erro ao desserializar pedido (Pickle)"]])

        if not isinstance(pedido_em_lista, list) or len(pedido_em_lista) != 4:
            return pickle.dumps([39902, ["Mensagem mal formada: estrutura inesperada"]])
        
        try:
            resposta_em_lista = self.processador.processa(pedido_em_lista)
        except Exception as e:
            print(f"SERVIDOR> Erro 39928: {e}")
            return pickle.dumps([39928, [str(e)]])

        try:
            resposta_bytes = pickle.dumps(resposta_em_lista)
            return resposta_bytes
        except Exception as e:
            print(f"SERVIDOR> Erro 39908: {e}")
            return pickle.dumps([39908, ["Erro ao serializar resposta (Pickle)"]])


    def get_loja(self):
        return self.loja
    
    def encerrar_servidor(self):
        print("SERVIDOR> A fechar ligações...")
        self.zookeeper.close() 
        self.rede.fechar_tudo()




        