from cliente.rede import TCPSocketCliente
import pickle

class Stub: 
    def __init__(self, ponto_acesso):
        self.rede = TCPSocketCliente(ponto_acesso)
        

    def processa(self, pedido):
        pedido_bytes = pickle.dumps(pedido)
        self.rede.enviar_mensagem(pedido_bytes)
        resposta_bytes = self.rede.receber_resposta()
        resposta = pickle.loads(resposta_bytes)
        return resposta
    
    def fechar_ligacao(self):
        self.rede.fechar()