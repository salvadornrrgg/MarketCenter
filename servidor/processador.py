# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Este ficheiro funciona como o Processador RPC, servindo de ponte entre o Skeleton e a Loja. Ele recebe pedidos estruturados em listas, valida as permissões do perfil e os códigos de operação. Após processar a lógica na Loja, constrói a resposta no formato [op_code_resposta, [dados]] para ser serializada e devolvida à rede
# -----------------------------

class Processador:

    def __init__(self, skeleton):
        self.skeleton = skeleton
        self.loja = self.skeleton.get_loja()
        
        self.HANDLERS = {
            10100: self._cmd_cria_categoria,
            10200: self._cmd_lista_categorias,
            10300: self._cmd_remove_categoria,
            10400: self._cmd_cria_produto,
            10500: self._cmd_lista_produtos,
            10600: self._cmd_aumenta_stock_produto,
            10700: self._cmd_atualiza_preco_produto,
            10800: self._cmd_cria_cliente,
            10900: self._cmd_lista_clientes,
            11000: self._cmd_adiciona_produto_carrinho,
            11100: self._cmd_remove_produto_carrinho,
            11200: self._cmd_lista_produtos_carrinho,
            11300: self._cmd_checkout_carrinho,
            11400: self._cmd_lista_encomendas
        }
    
    def processa(self, pedido_em_lista):
        
        try:
            if not isinstance(pedido_em_lista, list) or len(pedido_em_lista) != 4:
                return [39902, ["Mensagem mal formada"]]

            op_code = pedido_em_lista[0]
            argumentos = pedido_em_lista[1]
            id_perfil = pedido_em_lista[2]
            id_user = pedido_em_lista[3]

            if op_code in self.HANDLERS:
                
                return self.HANDLERS[op_code](argumentos, id_perfil, id_user)
            
            return [39901, ["Código de operação inválido"]]

        except Exception as e:
            return [39928, [str(e)]]
        

    #categorias 

    def _cmd_cria_categoria(self, argumentos, id_perfil, id_user):
        if id_perfil != 3: return [39920, []] 
        try:
            categoria = self.loja.criar_categoria(argumentos[0])
            return [20100, [categoria]]
        except Exception as e:
            return [30101, [str(e)]]
    
    #lista categorias
    def _cmd_lista_categorias(self, argumentos, id_perfil, id_user):
        categorias = list(self.loja.obter_todas_categorias().values())
        produtos = list(self.loja.obter_todos_produtos().values())
        return [20200, [categorias, produtos]]
        

    #remove categoria
    def _cmd_remove_categoria(self, argumentos, id_perfil, id_user):
        if id_perfil != 3: return [39920, []]
        try:
            self.loja.remove_categoria(argumentos[0])
            return [20300, []]
        except Exception as e:
            return [30301, [str(e)]]
        
    #produtos 

    #criar produto
    def _cmd_cria_produto(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, []] 
        try:
            produto = self.loja.criar_produto(argumentos[0], argumentos[1], argumentos[2], argumentos[3])
            return [20400, [produto]]
        except Exception as e:
            return [30401, [str(e)]]

    #lista produtos
    def _cmd_lista_produtos(self, argumentos, id_perfil, id_user):
        produtos = list(self.loja.obter_todos_produtos().values())
        categorias = list(self.loja.obter_todas_categorias().values())
        return [20500, [categorias, produtos]]

    #aumenta stock
    def _cmd_aumenta_stock_produto(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, []]
        try:
            produto = self.loja.aumentar_stock_produto(argumentos[0], argumentos[1])
            return [20600, [produto]]
        except Exception as e:
            return [30601, [str(e)]]
    
    #atualiza preco
    def _cmd_atualiza_preco_produto(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, []]
        try:
            produto = self.loja.atualizar_preco_produto(argumentos[0], argumentos[1])
            return [20700, [produto]]
        except Exception as e:
            return [30701, [str(e)]]


    #clientes 

    #cria cliente
    def _cmd_cria_cliente(self, argumentos, id_perfil, id_user):
        if id_perfil != 0: return [39920, []] 
        try:
            cliente = self.loja.criar_cliente(argumentos[0], argumentos[1], argumentos[2])
            return [20800, [cliente]]
        except Exception as e:
            return [30801, [str(e)]]


    #lista clientes
    def _cmd_lista_clientes(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, []]
        clientes = list(self.loja.obter_todos_clientes().values())
        return [20900, [clientes]]


    #Carrinho de compras 

    #adiciona produto ao carrinho
    def _cmd_adiciona_produto_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, []] 
        try:
            produto = self.loja.adicionar_produto_carrinho(id_user, argumentos[0], argumentos[1])
            return [21000, [produto]]
        except Exception as e:
            return [31001, [str(e)]]
        
    #remove produto do carrinho
    def _cmd_remove_produto_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, []]
        try:
            produto = self.loja.remover_produto_carrinho(id_user, argumentos[0])
            return [21100, [produto]]
        except Exception as e:
            return [31101, [str(e)]]

    
    #lista produtos do carrinho
    def _cmd_lista_produtos_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, []]
        try:
            categorias = list(self.loja.obter_todas_categorias().values())
            produtos = list(self.loja.obter_todos_produtos().values())
            return [21200, [categorias, produtos]]
        except Exception as e:
            return [31201, [str(e)]]

    #cria encomenda a partir do carrinho
    def _cmd_checkout_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, []]
        try:
            encomenda = self.loja.fazer_checkout_carrinho(id_user)
            return [21300, [encomenda]]
        except Exception as e:
            return [31301, [str(e)]]

    #lista todas as encomendas
    def _cmd_lista_encomendas(self, argumentos, id_perfil, id_user):
        if id_perfil == 0: return [39920, []] 
        try:
            id_alvo = argumentos[0] if id_perfil in [2, 3] and len(argumentos) > 0 else id_user
            cliente, encomendas = self.loja.obter_todas_encomendas(id_alvo)
            
            produtos_encomendas = [list(enc.produtos_carrinho.keys()) for enc in encomendas]
            return [21400, [encomendas, produtos_encomendas]]
        except Exception as e:
            return [31401, [str(e)]]
        
    
