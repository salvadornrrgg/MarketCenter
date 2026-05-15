from kazoo.client import KazooClient

class ZooKeeperClient(): 
    
    def __init__(self, funcao_avisar_stub, hosts_zk): 
        self.zk = KazooClient(hosts=hosts_zk)
        self.avisar_stub = funcao_avisar_stub
    
    def connect(self):         
        self.zk.start()
        print("Cliente ligado ao ZooKeeper!")

        #se houver mudanças(algum server saiu) sao definidos novos servers tail e head
        self.zk.ChildrenWatch("/chain", self.reagir_mudancas)


    def reagir_mudancas(self, children_nodes):
        print(f"\nCLIENTE-ZK> [VIGIA ATIVADO] A lista de servidores em /chain mudou!")
        
        if not children_nodes:
            print("CLIENTE-ZK> ALERTA: Não há servidores vivos na cadeia!")
            self.avisar_stub(None, None)
            return
        
        sorted_nodes = sorted(children_nodes)
        head_node = sorted_nodes[0]
        tail_node = sorted_nodes[-1]
        
        try:
            ponto_acesso_head = self.get(f"/chain/{head_node}")
            ponto_acesso_tail = self.get(f"/chain/{tail_node}")
            
            print(f"CLIENTE-ZK> Nova HEAD (Escritas): {ponto_acesso_head}")
            print(f"CLIENTE-ZK> Nova TAIL (Leituras): {ponto_acesso_tail}")
            
            self.avisar_stub(ponto_acesso_head, ponto_acesso_tail)
            
        except Exception as e:
            print(f"CLIENTE-ZK> Erro a ler dados dos nós: {e}")


    def get(self, path):
        dados, _ = self.zk.get(path)
        return dados.decode("utf-8")
            

    def close(self): 
        self.zk.stop()
        self.zk.close()
  
  
