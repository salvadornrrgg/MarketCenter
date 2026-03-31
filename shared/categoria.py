# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Este ficheiro define a estrutura de dados como se fosse um modelo, da entidade, armazenando os seus atributos essenciais e garantindo a correta criação dos mesmos na memória da aplicação.
# -----------------------------





class Categoria:
    _contador_global = 1

    def __init__(self, nome):
        self.id_categoria = Categoria._contador_global
        self.nome = nome
        Categoria._contador_global += 1

    def obter_id(self): 
        return self.id
