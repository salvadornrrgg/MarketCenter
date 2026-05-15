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
    
    def __init__(self, porto_servidor): 
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.ip_real = obter_ip_real()
        self.porto = porto_servidor
        self.znode = None
    
    def connect(self): 
        self.zk.start()
        print("Servidor ligado ao ZooKeeper!")

        self.create()

        dados_servidor = f"{self.ip_real}:{self.porto}".encode('utf-8')

        self.meu_znode = self.create_ephemeral("/chain/node", dados_servidor)

        print(f"SERVIDOR-ZK> Registado com sucesso! Nó: {self.znode}")
        print(f"SERVIDOR-ZK> IP/Porto anunciado: {self.ip_real}:{self.porto}")
    


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
        
        nome_znode = self.znode.replace(path, "")
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
    

    def close(self): 
        self.zk.stop()
        self.zk.close()

    



