# -----------------------------
# GRUPO 09    
# Salvador Gonçalves   64162
# Tomás Farinha        64253
# Este ficheiro é o "cérebro" do servidor. Ele recebe os pedidos 
# já descodificados pelo Skeleton e executa a lógica de negócio real na loja
# É aqui que se validam as permissões (quem pode criar o quê), 
# se alteram os stocks e se geram as encomendas. O processador decide 
# se a operação foi um sucesso, 2xxxx, ou um erro, série 3xxxx.
# -----------------------------

from shared.excepcoes import ExcepcaoBase
from shared.excepcoes import OpCodes

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
            if not isinstance(pedido_em_lista, list): 
                return [39903, ["Pedido não é uma lista"]]
            if len(pedido_em_lista) != 4: 
                return [39904, ["Pedido não tem 4 campos"]]

            op_code, argumentos, id_perfil, id_user = pedido_em_lista

            if not isinstance(argumentos, list): 
                return [39905, ["Argumentos devem ser uma lista"]]
            
            if id_perfil not in [0, 1, 2, 3]: 
                return [39906, ["Perfil inválido"]]

            if not isinstance(id_user, int) or id_user < 0:
                return [39907, ["ID de utilizador inválido ou mal formatado"]]

            if op_code in self.HANDLERS:
                return self.HANDLERS[op_code](argumentos, id_perfil, id_user)
            
            if op_code == OpCodes.SYNC_LOJA:
                estado = self.skeleton.get_loja().obter_estado()
                return [OpCodes.OK_SYNC_LOJA, estado]

            return [39901, ["Código de operação inválido"]]

        except Exception as e:
            return [39928, [str(e)]]


    # --- CATEGORIAS ---

    def _cmd_cria_categoria(self, argumentos, id_perfil, id_user):
        if id_perfil != 3: return [39920, ["Apenas o Administrador pode criar categorias."]] 
        if len(argumentos) < 1: return [39914, ["Falta o nome da categoria"]]
        try:
            categoria = self.loja.criar_categoria(argumentos[0])
            return [20100, [categoria]]
        except ExcepcaoBase as e: return [e.code, [e.msg]] 
        except Exception as e: return [30101, [str(e)]] 
    
    def _cmd_lista_categorias(self, argumentos, id_perfil, id_user):
        try:
            categorias = list(self.loja.obter_todas_categorias().values())
            produtos = list(self.loja.obter_todos_produtos().values())
            return [20200, [categorias, produtos]]
        except Exception as e: return [30201, [str(e)]]

    def _cmd_remove_categoria(self, argumentos, id_perfil, id_user):
        if id_perfil != 3: return [39920, ["Apenas o Administrador pode remover categorias."]]
        if len(argumentos) < 1: return [39914, ["Falta o nome da categoria"]]
        try:
            self.loja.remove_categoria(argumentos[0])
            return [20300, []]
        except ExcepcaoBase as e: return [e.code, [e.msg]] 
        except Exception as e: return [30301, [str(e)]]
        

    # --- PRODUTOS ---

    def _cmd_cria_produto(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, ["Acesso negado: Perfil insuficiente para criar produtos."]]
        if len(argumentos) < 4: return [39914, ["Faltam dados: Nome, Categoria, Preço, Stock."]]
        try:
            nome_prod = argumentos[0]
            nome_cat = argumentos[1]
            preco = float(argumentos[2]) 
            quantidade = int(argumentos[3])
            
            produto = self.loja.criar_produto(nome_prod, nome_cat, preco, quantidade)
            return [20400, [produto]]
        except (ValueError, TypeError):
            return [39915, ["Preço (decimal) ou Stock (inteiro) com formato inválido."]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [30401, [str(e)]]

    def _cmd_lista_produtos(self, argumentos, id_perfil, id_user):
        try:
            produtos = list(self.loja.obter_todos_produtos().values())
            categorias = list(self.loja.obter_todas_categorias().values())
            return [20500, [categorias, produtos]]
        except Exception as e: return [30501, [str(e)]]

    def _cmd_aumenta_stock_produto(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, ["Acesso negado para aumentar stock."]]
        if len(argumentos) < 2: return [39914, ["Faltam argumentos: nome e quantidade"]]
        try:
            qtd = int(argumentos[1])
            produto = self.loja.aumentar_stock_produto(argumentos[0], qtd)
            return [20600, [produto]]
        except (ValueError, TypeError): return [39915, ["A quantidade deve ser um número inteiro."]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [30601, [str(e)]]
    
    def _cmd_atualiza_preco_produto(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, ["Acesso negado para atualizar preços."]]
        if len(argumentos) < 2: return [39914, ["Faltam argumentos: nome e preço"]]
        try:
            preco = float(argumentos[1])
            produto = self.loja.atualizar_preco_produto(argumentos[0], preco)
            return [20700, [produto]]
        except (ValueError, TypeError): return [39915, ["O preço deve ser um número decimal."]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [30701, [str(e)]]


    # --- CLIENTES ---

    def _cmd_cria_cliente(self, argumentos, id_perfil, id_user):
        if id_perfil != 0: return [39920, ["Apenas utilizadores anónimos podem registar novos clientes."]] 
        if len(argumentos) < 3: return [39914, ["Faltam argumentos: nome, email e pass"]]
        try:
            cliente = self.loja.criar_cliente(argumentos[0], argumentos[1], argumentos[2])
            return [20800, [cliente]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [30801, [str(e)]]

    def _cmd_lista_clientes(self, argumentos, id_perfil, id_user):
        if id_perfil not in [2, 3]: return [39920, ["Apenas Admin/Funcionário podem listar clientes."]]
        try:
            clientes = list(self.loja.obter_todos_clientes().values())
            return [20900, [clientes]]
        except Exception as e: return [30901, [str(e)]]


    # --- CARRINHO ---

    def _cmd_adiciona_produto_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, ["Esta operação exige um utilizador autenticado."]] 
        if len(argumentos) < 2: return [39914, ["Faltam argumentos: nome e quantidade"]]
        if type(argumentos[0]) is not str or type(argumentos[1]) is not int:
            return [39915, ["Tipos de argumentos inválidos (esperado: string, int)."]]
        try:
            nome_produto = argumentos[0]
            quantidade = int(argumentos[1]) 
            produto = self.loja.adicionar_produto_carrinho(id_user, nome_produto, quantidade)
            return [21000, [produto]]
        except (ValueError, TypeError): return [39915, ["Quantidade inválida."]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [31001, [str(e)]]
        
    def _cmd_remove_produto_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, ["Esta operação exige um utilizador autenticado."]]
        if len(argumentos) < 1: return [39914, ["Falta o nome do produto"]]
        try:
            produto = self.loja.remover_produto_carrinho(id_user, argumentos[0])
            return [21100, [produto]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [31101, [str(e)]]

    def _cmd_lista_produtos_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, ["Operação exige login de cliente."]]
        try:
            categorias = list(self.loja.obter_todas_categorias().values())

            obje_carrinho = self.loja.obter_todos_produtos_carrinho(id_user)
            
            return [21200, [categorias, obje_carrinho]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]

    def _cmd_checkout_carrinho(self, argumentos, id_perfil, id_user):
        if id_perfil != 1: return [39921, ["Apenas clientes podem efetuar checkout."]]
        try:
            encomenda = self.loja.fazer_checkout_carrinho(id_user)
            return [21300, [encomenda]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [31301, [str(e)]]


    # --- ENCOMENDAS ---

    def _cmd_lista_encomendas(self, argumentos, id_perfil, id_user):
        if id_perfil == 0: return [39920, ["Acesso negado para utilizadores anónimos."]] 
        try:
            id_alvo = argumentos[0] if id_perfil in [2, 3] and len(argumentos) > 0 else id_user
            cliente, encomendas, produtos_encomendas = self.loja.obter_todas_encomendas(id_alvo)

            return [21400, [encomendas, produtos_encomendas]]
        except ExcepcaoBase as e: return [e.code, [e.msg]]
        except Exception as e: return [31401, [str(e)]]