# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    # Este ficheiro é o "tradutor" do lado do servidor. 
    # Ele recebe as mensagens da rede em bytes, desserializa a informação e 
    # entrega o pedido ao Processador. Após a execução, volta a empacotar a 
    # resposta para enviar ao cliente. Além disso, gere a Chain Replication: 
    # encaminha operações de escrita para o servidor sucessor e trata da 
    # sincronização do estado da Loja quando o servidor se liga à cadeia.
    # -----------------------------

from servidor.rede import TCPSocketServidor
from cliente.rede import TCPSocketCliente
from shared.socket_utilities import PontoAcesso
from servidor.loja import Loja
from servidor.processador import Processador
from shared.excepcoes import OpCodes
import pickle
from servidor.zookeeperServidor import ZooKeeperServidor
import threading

class Skeleton:

    def __init__(self, ponto_acesso, hosts_zk):
        self.rede = TCPSocketServidor(ponto_acesso)
        self.loja = Loja()
        self.processador = Processador(self)
        self.zookeeper = ZooKeeperServidor(ponto_acesso.porto, self.atualizar_ligacoes, hosts_zk)
        self.ligacao_sucessor = None
        self.lock_escritas = threading.Lock()

    def atualizar_ligacoes(self, ponto_acesso_sucessor):
        print("SKELETON> O ZooKeeper avisou-me de mudanças! A reconfigurar ligações...")

        if self.ligacao_sucessor:
            self.ligacao_sucessor.fechar()
            self.ligacao_sucessor = None
        
        if ponto_acesso_sucessor:
            ip_sucessor, port_sucessor = ponto_acesso_sucessor.split(":")
            self.ligacao_sucessor = TCPSocketCliente(PontoAcesso(ip_sucessor, int(port_sucessor)))
            print(f"SKELETON> [SUCESSOR ATUALIZADO] Ligação permanente aberta para {ponto_acesso_sucessor}")
        else:
            print("SKELETON> [SUCESSOR ATUALIZADO] Sou a cauda (Tail). Não tenho sucessor.")



    def iniciar_servidor(self):
        print("SERVIDOR> A iniciar serviços...")
        self.zookeeper.connect()

        dados_antecessor = self.zookeeper.get_antecessor("/chain")
        
        #TEM antecessor?
        if dados_antecessor:
            print(f"SKELETON> A sincronizar estado com o antecessor: {dados_antecessor}")
            
            ip_antecessor, port_antecessor = dados_antecessor.split(":")
            pontoacesso_antecessor = PontoAcesso(ip_antecessor, int(port_antecessor))

            ligacao_antecessor = TCPSocketCliente(pontoacesso_antecessor)
        
            try:
                pedido = [OpCodes.SYNC_LOJA, [], 0, 0]

                self.enviar_mensagem(pedido, ligacao_antecessor)

                resposta = self.receber_resposta(ligacao_antecessor)

                op_code_resposta = resposta[0]
                dados_resposta = resposta[1]

                if op_code_resposta == OpCodes.OK_SYNC_LOJA: 
                    self.loja.importar_estado(dados_resposta)
                    print("SKELETON> Sincronização da loja concluída!")
                else:
                    print(f"SKELETON> Falha na sincronização. O antecessor respondeu com erro: {op_code_resposta}")
                
            finally:
                ligacao_antecessor.fechar()
        else:
            print("SKELETON> Sou a Head da cadeia. Não há sincronização inicial.")
        
        self.rede.aceitar(self.processa_pedido)



    def processa_pedido(self, pedido_bytes):
        try:
            pedido_em_lista = pickle.loads(pedido_bytes)
        except Exception as e:
            print(f"SERVIDOR> Erro 39909: {e}")
            return pickle.dumps([39909, ["Erro ao desserializar pedido (Pickle)"]])

        if not isinstance(pedido_em_lista, list) or len(pedido_em_lista) != 4:
            return pickle.dumps([39902, ["Mensagem mal formada: estrutura inesperada"]])
        
        op_code = pedido_em_lista[0]

        try:
            if self.is_leitura(op_code):
                resposta_em_lista = self.processador.processa(pedido_em_lista)
            else:
                with self.lock_escritas:
                    resposta_em_lista = self.processador.processa(pedido_em_lista)
                    
                    if self.ligacao_sucessor and str(resposta_em_lista[0]).startswith('2'):
                        self.enviar_mensagem(pedido_em_lista, self.ligacao_sucessor)
                        
                        resposta_em_lista = self.receber_resposta(self.ligacao_sucessor)
        
        
        except Exception as e:
            print(f"SERVIDOR> Erro 39928: {e}")
            return pickle.dumps([39928, [str(e)]])


        try:
            resposta_bytes = pickle.dumps(resposta_em_lista)
            return resposta_bytes
        except Exception as e:
            print(f"SERVIDOR> Erro 39908: {e}")
            return pickle.dumps([39908, ["Erro ao serializar resposta (Pickle)"]])


    def is_leitura(self, op_code):
        op_codes_leitura = [
            OpCodes.LISTA_CATEGORIAS,
            OpCodes.LISTA_PRODUTOS,
            OpCodes.LISTA_CLIENTES,
            OpCodes.LISTA_CARRINHO,
            OpCodes.LISTA_ENCOMENDAS
        ]
        return op_code in op_codes_leitura

    def get_loja(self):
        return self.loja
    
    def encerrar_servidor(self):
        print("SERVIDOR> A fechar ligações...")
        self.zookeeper.close() 
        self.rede.fechar_tudo()

    def enviar_mensagem(self, pedido, socket_a_usar):
        pedido_bytes = pickle.dumps(pedido)
        socket_a_usar.enviar_pedido(pedido_bytes)

    def receber_resposta(self, socket_a_usar):
        resposta_bytes = socket_a_usar.receber_resposta()
        resposta = pickle.loads(resposta_bytes)
        return resposta


        