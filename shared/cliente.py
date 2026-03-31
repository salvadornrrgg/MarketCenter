# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Este ficheiro define a estrutura de dados como se fosse um modelo, da entidade, armazenando os seus atributos essenciais e garantindo a correta criação dos mesmos na memória da aplicação.
# -----------------------------


class Cliente:
    _contador_global = 1

    def __init__(self, nome, email, password):
        self.id_cliente = Cliente._contador_global
        self.nome = nome
        self.email = email
        self.password = password
        self.carrinho_compras = {}
        Cliente._contador_global += 1

    def obter_id(self): 
        return self.id_cliente
