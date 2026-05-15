# -----------------------------
    # GRUPO 09    
    # Salvador Gonçalves   64162
    # Tomás Farinha        64253
    # Este ficheiro atua como o representante do servidor no cliente. 
    # Para o Processador, parece que as funções da loja estão a correr localmente, 
    # mas na verdade, o Stub apenas serializa (empacota) os dados e envia-os pela 
    # rede. Além disso, é ele que faz a gestão inteligente do trânsito: encaminha 
    # as operações de escrita para a Head e as de leitura para a Tail!
# -----------------------------

from cliente.rede import TCPSocketCliente
from cliente.zookeeperCliente import ZooKeeperClient
from shared.excepcoes import OpCodes
from shared.socket_utilities import PontoAcesso
import pickle


class Stub: 
    def __init__(self, hosts_zk):
        self.rede_head = None
        self.rede_tail = None
        self.zookeeper = ZooKeeperClient(self.atualizar_ligacoes, hosts_zk)
        self.zookeeper.connect()
        
    def atualizar_ligacoes(self, ponto_acesso_head, ponto_acesso_tail):
        print("STUB> O ZooKeeper avisou-me de mudanças! A reconfigurar ligações...")

        if self.rede_head:
            self.rede_head.fechar()

        if self.rede_tail:
            self.rede_tail.fechar()

        if ponto_acesso_head and ponto_acesso_tail:
            ip_head, port_head = ponto_acesso_head.split(":")
            self.rede_head = TCPSocketCliente(PontoAcesso(ip_head, int(port_head)))
            
            ip_tail, port_tail = ponto_acesso_tail.split(":")
            self.rede_tail = TCPSocketCliente(PontoAcesso(ip_tail, int(port_tail)))
            print("STUB> Ligações permanentes à Head e Tail estabelecidas com sucesso!")


    def processa(self, pedido):
        op_code = pedido[0]
        
        if self.is_leitura(op_code):
            print("STUB> Operação de Leitura. A encaminhar pela ligação TAIL...")
            socket_a_usar = self.rede_tail
        else:
            print("STUB> Operação de Escrita. A encaminhar pela ligação HEAD...")
            socket_a_usar = self.rede_head
        
        if not socket_a_usar:
            print("STUB> Erro crítico: Não há servidores disponíveis na rede.")
            return None

        try:
            self.enviar_mensagem(pedido, socket_a_usar)
            resposta = self.receber_resposta(socket_a_usar)
            return resposta
        except Exception as e:
            print(f"STUB> Erro na comunicação com o servidor: {e}")
            return [OpCodes.ERRO_GENERICO, ["Falha de ligação ao servidor."]]


    
    def is_leitura(self, op_code):
        op_codes_leitura = [
            OpCodes.LISTA_CATEGORIAS,
            OpCodes.LISTA_PRODUTOS,
            OpCodes.LISTA_CLIENTES,
            OpCodes.LISTA_CARRINHO,
            OpCodes.LISTA_ENCOMENDAS
        ]
        return op_code in op_codes_leitura

    def enviar_mensagem(self, pedido, socket_a_usar):
        pedido_bytes = pickle.dumps(pedido)
        socket_a_usar.enviar_pedido(pedido_bytes)

    def receber_resposta(self, socket_a_usar):
        resposta_bytes = socket_a_usar.receber_resposta()
        resposta = pickle.loads(resposta_bytes)
        return resposta

    def fechar_ligacao(self):
        if self.rede_head: 
            self.rede_head.fechar()

        if self.rede_tail: 
            self.rede_tail.fechar()
            
        self.zookeeper.close()

    