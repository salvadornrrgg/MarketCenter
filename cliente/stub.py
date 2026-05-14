from cliente.rede_c import TCPSocketCliente
import pickle

class Stub: 
    def __init__(self, ponto_acesso):
        self.rede = TCPSocketCliente(ponto_acesso)
        

    def processa(self, pedido):
        self.enviar_mensagem(pedido)
        return self.receber_resposta()
    
    
    def enviar_mensagem(self, pedido):
        pedido_bytes = pickle.dumps(pedido)
        self.rede.enviar_pedido(pedido_bytes)

    def receber_resposta(self):
        resposta_bytes = self.rede.receber_resposta()
        resposta = pickle.loads(resposta_bytes)
        return resposta

    
    def fechar_ligacao(self):
        self.rede.fechar()