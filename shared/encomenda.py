# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Este ficheiro define a estrutura de dados como se fosse um modelo, da entidade, armazenando os seus atributos essenciais e garantindo a correta criação dos mesmos na memória da aplicação.
# -----------------------------


class Encomenda:
    _contador_global = 1

    def __init__(self, id_cliente, produtos_carrinho, total, data):
        self.id_encomenda = Encomenda._contador_global
        self.id_cliente = id_cliente
        self.produtos = produtos_carrinho
        self.total_preco = total
        self.data = data
        Encomenda._contador_global += 1

    def obter_id(self): 
        return self.id
