class Produto:
    _contador_global = 1

    def __init__(self, nome, categoria, preco, quantidade):
        self.id_produto = Produto._contador_global
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade
        Produto._contador_global += 1

    def obter_id(self): 
        return self.id
