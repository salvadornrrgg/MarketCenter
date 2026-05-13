# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Este ficheiro é o "cérebro" da loja, é onde se aplicam as regras do negócio, onde são guardados, agora nesta fase, os dados em memoria em varios dicionarios, aqui é onde implementamos as funçoes que efetuam as condiçoes dos comandos escritos nas tabelas do enuciado
# -----------------------------
import copy
from shared.utilities import normalizar_nome
from shared.excepcoes import (
    CategoriaJaExiste,
    CategoriaNaoExiste,
    CategoriaNomeInvalido,
    CategoriaComProdutos,
    ProdutoJaExiste,
    ProdutoNaoExiste,
    PrecoInvalido,
    QuantidadeInvalida,
    ClienteNaoExiste,
    EmailJaExiste,
    StockInsuficiente,
    QuantidadeCarrinhoInvalida,
    ProdutoNaoNoCarrinho,
    CarrinhoVazio
)
from shared.categoria import Categoria
from shared.produto import Produto
from shared.cliente import Cliente
from shared.encomenda import Encomenda
from datetime import datetime

class Loja:

    def __init__(self):
        self._categorias = {}
        self._produtos = {}
        self._clientes = {}
        self._encomendas = {}

    def reset(self): 
        Categoria._contador_global = 1
        Produto._contador_global = 1
        Cliente._contador_global = 1
        Encomenda._contador_global = 1
        
        self._categorias.clear()
        self._produtos.clear()
        self._clientes.clear()
        self._encomendas.clear()


    # -----------------------------
    # Categorias
    # -----------------------------

    def criar_categoria(self, nome):
        nome = normalizar_nome(nome)
        if self.obter_id_categoria(nome) is not None:
            raise CategoriaJaExiste(nome)
        categoria = Categoria(nome)
        self._categorias[categoria.id_categoria] = categoria
        return categoria
    
    #lista categorias 
    def obter_todas_categorias(self):
        return self._categorias
    
    #funçao auxiliar para LISTA_CATEGORIAS
    def obter_total_produtos_por_categoria(self, categoria):
        contador = 0
        for produto in self._produtos.values():
            if produto.categoria == categoria:
                contador += 1
        return contador
    
    #remove categoria
    def remove_categoria(self, nome):
        nome = normalizar_nome(nome)
        if not nome:
            raise CategoriaNomeInvalido()
        idcategoria = self.obter_id_categoria(nome)
        if idcategoria is None:
            raise CategoriaNaoExiste(nome)
        if self.verifica_categoria_produtos_em_stock(nome):
            raise CategoriaComProdutos(nome)
        
        del self._categorias[idcategoria]
        return nome
    

     #funçao auxiliar para REMOVER_CATEGORIA
    def verifica_categoria_produtos_em_stock (self, nome_categoria):
        for produto in self._produtos.values():
            if produto.categoria == nome_categoria:
                return True
        return False
    

    def obter_id_categoria(self, nome): 
        for categoria in self._categorias.values(): 
            if nome == categoria.nome: 
                return categoria.id_categoria
        return None
    
    # -----------------------------
    # Produtos
    # -----------------------------
    
    #cria produto
    def criar_produto(self, nome_produto, nome_categoria, preco, quantidade):
        nome_produto = normalizar_nome(nome_produto)
        nome_categoria = normalizar_nome(nome_categoria)
        preco = round(preco, 2)

        if preco <= 0:
            raise PrecoInvalido()
        if quantidade < 0:
            raise QuantidadeInvalida()
        if self.obter_id_categoria(nome_categoria) is None:
            raise CategoriaNaoExiste(nome_categoria)
        if self.obter_id_produto(nome_produto) is not None:
            raise ProdutoJaExiste(nome_produto)
        
        produto = Produto(nome_produto, nome_categoria, preco, quantidade)
        self._produtos[produto.id_produto] = produto

        return produto

    
    #lista todos os produtos
    def obter_todos_produtos(self):
        return self._produtos
    

    #funçao auxiliar para LISTA_PRODUTOS
    def obter_total_quantidade(self):
        quantidade_total = 0
        for produto in self._produtos.values():
            quantidade_total += produto.quantidade
        return quantidade_total


    #aumenta stock de produto
    def aumentar_stock_produto(self, nome_produto, add_quantidade):
        nome_produto = normalizar_nome(nome_produto)
        id_produto = self.obter_id_produto(nome_produto)

        if id_produto is None:
            raise ProdutoNaoExiste(nome_produto)
        if add_quantidade <= 0:
            raise QuantidadeInvalida()

        produto = self._produtos[id_produto]
        produto.quantidade += add_quantidade

        return produto 
    

    #atualiza preco de produto
    def atualizar_preco_produto(self, nome_produto, novo_preco):
        nome_produto = normalizar_nome(nome_produto)
        novo_preco = round(novo_preco, 2)

        id_produto = self.obter_id_produto(nome_produto)

        if id_produto is None:
            raise ProdutoNaoExiste(nome_produto)

        if novo_preco <= 0:
            raise PrecoInvalido()

        produto = self._produtos[id_produto]
        produto.preco = novo_preco

        return produto


    def obter_id_produto(self, nome):
        for produto in self._produtos.values(): 
            if nome == produto.nome:
                return produto.id_produto
        return None


    # -----------------------------
    # Clientes
    # -----------------------------
    
    #cria cliente
    def criar_cliente(self, nome_cliente, email, password):
        nome_cliente = normalizar_nome(nome_cliente)
        email = email.lower()

        for cliente in self._clientes.values():
            if cliente.email.lower() == email:
                raise EmailJaExiste()

        cliente = Cliente(nome_cliente, email, password)
        self._clientes[cliente.id_cliente] = cliente

        return cliente
    
    #listar clientes
    def obter_todos_clientes(self):
        return self._clientes

    # -----------------------------
    # Carrinho de compras
    # -----------------------------

    #adicionar produto ao carrinho
    def adicionar_produto_carrinho(self, id_cliente, nome_produto, quantidade):
        id_cliente = int(id_cliente)
        nome_produto = normalizar_nome(nome_produto)

        if id_cliente  not in self._clientes:
            raise ClienteNaoExiste()
        cliente = self._clientes[id_cliente]

        id_produto = self.obter_id_produto(nome_produto)
        if id_produto is None:
            raise ProdutoNaoExiste(nome_produto)
        produto = self._produtos[id_produto]

        if quantidade <= 0:
            raise QuantidadeCarrinhoInvalida()

        if quantidade > produto.quantidade:
            raise StockInsuficiente()

        produto.quantidade -= quantidade

        if id_produto in cliente.carrinho_compras:
            cliente.carrinho_compras[id_produto] += quantidade
        else:
            cliente.carrinho_compras[id_produto] = quantidade

        return produto
    
    #remover produto do carrinho
    def remover_produto_carrinho(self, id_cliente, nome_produto):
        id_cliente = int(id_cliente)
        nome_produto = normalizar_nome(nome_produto)

        if id_cliente  not in self._clientes:
            raise ClienteNaoExiste ()
        cliente = self._clientes[id_cliente]

        id_produto = self.obter_id_produto(nome_produto)
        if id_produto is None:
            raise ProdutoNaoExiste()
        produto = self._produtos[id_produto]

        if id_produto not in cliente.carrinho_compras:
            raise ProdutoNaoNoCarrinho()
        
        quantidade_reposta = cliente.carrinho_compras[id_produto]
        produto.quantidade += quantidade_reposta
        del cliente.carrinho_compras[id_produto]

        return produto
    
    #obter todos os produtos do carrinho
    def obter_todos_produtos_carrinho(self, id_cliente):
        id_cliente = int(id_cliente)

        if id_cliente  not in self._clientes:
            raise ClienteNaoExiste()
        cliente = self._clientes[id_cliente]

        lista_objetos_produto = []
        
        for id_prod, quantidade_no_carrinho in cliente.carrinho_compras.items():
            produto_original = self._produtos[id_prod]

            produto_para_rede = copy.copy(produto_original)
            
            produto_para_rede.quantidade = quantidade_no_carrinho

            lista_objetos_produto.append(produto_para_rede)

        return lista_objetos_produto

    #fazer checkout do carrinho de compras
    def fazer_checkout_carrinho(self, id_cliente):
        id_cliente = int(id_cliente)

        if id_cliente  not in self._clientes:
            raise ClienteNaoExiste()
        cliente = self._clientes[id_cliente]

        produtos_carrinho = len(cliente.carrinho_compras)
        if produtos_carrinho < 1:
            raise CarrinhoVazio()
        
        total_valor_encomenda = 0.00
        for id_produto, quantidade in cliente.carrinho_compras.items():
            produto = self._produtos[id_produto]
            total_valor_encomenda += round(produto.preco * quantidade, 2)
        
        total_valor_encomenda = round(total_valor_encomenda, 2)

        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        produtos_encomenda = cliente.carrinho_compras.copy()

        encomenda_nova = Encomenda(id_cliente, produtos_encomenda, total_valor_encomenda, data_atual)
        self._encomendas[encomenda_nova.id_encomenda] = encomenda_nova
        
        cliente.carrinho_compras.clear()

        return encomenda_nova

    # -----------------------------
    # Encomendas
    # -----------------------------

    #Listar encomendas
    def obter_todas_encomendas(self, id_cliente):
        id_cliente = int(id_cliente)

        if id_cliente  not in self._clientes:
            raise ClienteNaoExiste()
        cliente = self._clientes[id_cliente]

        encomendas_cliente = []
        produtos_das_encomendas = []
        for encomenda in self._encomendas.values():
            if encomenda.id_cliente == id_cliente:
                encomendas_cliente.append(encomenda)

                lista_prods_desta_encomenda = []
                for id_prod, qtd_comprada in encomenda.produtos.items():
                    produto_original = self._produtos[id_prod]
                    
                    produto_para_rede = copy.copy(produto_original)
                    produto_para_rede.quantidade = qtd_comprada 
                    
                    lista_prods_desta_encomenda.append(produto_para_rede)
                
                produtos_das_encomendas.append(lista_prods_desta_encomenda)
        
        return cliente, encomendas_cliente, produtos_das_encomendas
       
        
        