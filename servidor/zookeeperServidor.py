# -----------------------------
    # GRUPO 09    
    # Salvador Gonçalves   64162
    # Tomás Farinha        64253
    # Este ficheiro é o que trata do ZooKeeper. 
    # É ele que vai à pasta "/chain" identificar IP/Porto. Também fica a vigiar a vizinhança: 
    # se entrar ou sair algum servidor da cadeia, ele avisa imediatamente 
    # o Skeleton para recalcular quem é a Head, a Tail e a quem se deve ligar.
# -----------------------------

import socket
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError

def obter_ip_real():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class ZooKeeperServidor(): 
    
    def __init__(self, porto_servidor, funcao_avisar_skeleton, hosts_zk): 
        self.zk = KazooClient(hosts=hosts_zk)
        self.ip_real = obter_ip_real()
        self.porto = porto_servidor
        self.znode = None
        self.avisar_skeleton = funcao_avisar_skeleton
    
    def connect(self): 
        self.zk.start()
        print("Servidor ligado ao ZooKeeper!")
        self.create()

        dados_servidor = f"{self.ip_real}:{self.porto}".encode('utf-8')

        self.znode = self.create_ephemeral("/chain/node", dados_servidor)

        print(f"SERVIDOR-ZK> Registado com sucesso! Nó: {self.znode}")
        print(f"SERVIDOR-ZK> IP/Porto anunciado: {self.ip_real}:{self.porto}")

        #se houver mudanças sao definidos novos servers tail e head
        self.zk.ChildrenWatch("/chain", self.reagir_mudancas)

        
    def reagir_mudancas(self, children_nodes):
        print("SERVIDOR-ZK> [WATCHER] A cadeia foi alterada! A recalcular sucessor...")
        ponto_acesso_sucessor = self.get_sucessor("/chain") 
        self.avisar_skeleton(ponto_acesso_sucessor)

    def create(self):
        if not self.zk.exists("/chain"):
            try:
                self.zk.create("/chain", b"")
            except NodeExistsError:
                pass


    def create_ephemeral(self, path, value): 
        return self.zk.create(
            path, 
            value, 
            ephemeral=True, 
            sequence=True
        )
    

    def get(self, path):
        dados, _ = self.zk.get(path)
        return dados.decode("utf-8")

    def get_sucessor(self, path): 
        children_nodes = self.zk.get_children(path)
        if not children_nodes: 
            return None
        
        nome_znode = self.znode.replace(f"{path}/", "")
        sorted_nodes = sorted(children_nodes)

        try:
            posicao = sorted_nodes.index(nome_znode)
        except ValueError:
            return None
        
        if posicao < (len(sorted_nodes) - 1):
            noSucessor = sorted_nodes[posicao + 1]

            conteudoNoSucessor = self.get(f"{path}/{noSucessor}")
            return conteudoNoSucessor

        #É o último da fila (caude) não tem sucessor
        return None
    
    def get_antecessor(self, path):
        children_nodes = self.zk.get_children(path)
        if not children_nodes: 
            return None
        
        nome_znode = self.znode.replace(f"{path}/", "")
        sorted_nodes = sorted(children_nodes)

        try:
            posicao = sorted_nodes.index(nome_znode)
        except ValueError:
            return None
        
        if posicao > 0:
            noAntecessor = sorted_nodes[posicao - 1]

            conteudoNoAntecessor = self.get(f"{path}/{noAntecessor}")
            return conteudoNoAntecessor

        #É o primeiro da fila (head) não tem antecessor
        return None
    

    def close(self): 
        self.zk.stop()
        self.zk.close()

    



