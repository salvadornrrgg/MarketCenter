# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Este ficheiro faz a ponte entre o main e o stub, faz com que o main nao tenha tanto codigo e nao tenha que realizar/articular o pedido em lista. Ele recebe o pedido em sting e divide o em varios pedaços e manda pra o stub o pedido em lista
# -----------------------------
from cliente.stub import Stub
import shlex
from  shared.socket_utilities import PontoAcesso
from shared.excepcoes import (OpCodes, ComandoDesconhecido, ComandoMalFormado, 
    ComandoVazio, NumeroArgumentosInvalido, TipoArgumentoInvalido, ValorArgumentoInvalido, 
    PrecoInvalido, QuantidadeInvalida, QuantidadeCarrinhoInvalida, EmailInvalido, PasswordInvalida, 
    CategoriaJaExiste, CategoriaNaoExiste, CategoriaComProdutos, ProdutoJaExiste, ProdutoNaoExiste, 
    ClienteNaoExiste, EmailJaExiste, StockInsuficiente, ProdutoNaoNoCarrinho, CarrinhoVazio, FalhaEncomenda, 
    ErroInterno, OperacaoNaoAutorizada, UtilizadorNaoAutenticado)



class Processador:

    def __init__(self, PontoAcesso, id_perfil, id_user):
        self.stub = Stub(PontoAcesso)
        self.idPerfil = id_perfil
        self.id_user = id_user

        self.codigos_operacoes = {
            "CRIA_CATEGORIA": OpCodes.CRIA_CATEGORIA,
            "LISTA_CATEGORIAS": OpCodes.LISTA_CATEGORIAS,
            "REMOVE_CATEGORIA": OpCodes.REMOVE_CATEGORIA,
            "CRIA_PRODUTO": OpCodes.CRIA_PRODUTO,
            "LISTA_PRODUTOS": OpCodes.LISTA_PRODUTOS,
            "AUMENTA_STOCK_PRODUTO": OpCodes.AUMENTA_STOCK,
            "ATUALIZA_PRECO_PRODUTO": OpCodes.ATUALIZA_PRECO,
            "CRIA_CLIENTE": OpCodes.CRIA_CLIENTE,
            "LISTA_CLIENTES": OpCodes.LISTA_CLIENTES,
            "ADICIONA_PRODUTO_CARRINHO": OpCodes.ADICIONA_PRODUTO_CARRINHO,
            "REMOVE_PRODUTO_CARRINHO": OpCodes.REMOVE_PRODUTO_CARRINHO,
            "LISTA_CARRINHO": OpCodes.LISTA_CARRINHO,
            "CHECKOUT_CARRINHO": OpCodes.CHECKOUT_CARRINHO,
            "LISTA_ENCOMENDAS": OpCodes.LISTA_ENCOMENDAS,
        }

    
    def processa(self, pedido_user):
        pedido_partido = shlex.split(pedido_user)
        if not pedido_partido:
            return ""
            
        comando = pedido_partido[0].upper()
        argumentos = pedido_partido[1:]

        if comando not in self.codigos_operacoes:
            raise ComandoDesconhecido(comando)            

        op_code = self.codigos_operacoes[comando]

        pedido_em_lista = [op_code, argumentos, self.idPerfil, self.id_user]
        print(f"Pedido:  {pedido_em_lista}")

        resposta = self.stub.processa(pedido_em_lista)

        op_code_resposta = resposta[0]
        lista_resposta = resposta[1]

        argumento = lista_resposta[0] if len(lista_resposta) > 0 else ""

        #Erros

        if op_code_resposta >= 30000:
            
            if op_code_resposta == OpCodes.OP_CODE_INVALIDO:
                raise ComandoDesconhecido(argumento)
            
            elif op_code_resposta == OpCodes.MENSAGEM_MAL_FORMADA:
                raise ComandoMalFormado(argumento)
            
            elif op_code_resposta == OpCodes.NUMERO_ARGUMENTOS_INVALIDO:
                arg2 = lista_resposta[1] if len(lista_resposta) > 1 else ""
                raise NumeroArgumentosInvalido(argumento, arg2)
            
            elif op_code_resposta == OpCodes.TIPO_ARGUMENTO_INVALIDO:
                raise TipoArgumentoInvalido(argumento)
            
            elif op_code_resposta == OpCodes.VALOR_ARGUMENTO_INVALIDO:
                raise ValorArgumentoInvalido(argumento if argumento else "Valor inválido.")
            
            elif op_code_resposta == OpCodes.ARGUMENTO_VAZIO:
                raise ComandoVazio()
            
            elif op_code_resposta == OpCodes.OPERACAO_NAO_AUTORIZADA:
                raise OperacaoNaoAutorizada()
            
            elif op_code_resposta == OpCodes.UTILIZADOR_NAO_AUTENTICADO:
                raise UtilizadorNaoAutenticado()
                
            elif op_code_resposta == OpCodes.ERRO_INTERNO_SERVIDOR:
                raise ErroInterno(argumento if argumento else "Erro interno do servidor.")

            elif op_code_resposta == OpCodes.CATEGORIA_JA_EXISTE:
                raise CategoriaJaExiste(argumento)
            elif op_code_resposta == OpCodes.CATEGORIA_NAO_EXISTE:
                raise CategoriaNaoExiste(argumento)
            elif op_code_resposta == OpCodes.CATEGORIA_COM_PRODUTOS:
                raise CategoriaComProdutos(argumento)

            elif op_code_resposta == OpCodes.PRODUTO_JA_EXISTE:
                raise ProdutoJaExiste(argumento)

            elif op_code_resposta in [OpCodes.PRODUTO_NAO_EXISTE, OpCodes.PRODUTO_NAO_EXISTE_PRECO, OpCodes.PRODUTO_NAO_EXISTE_CARRINHO, OpCodes.PRODUTO_NAO_EXISTE_REMOVE]:
                raise ProdutoNaoExiste(argumento)
            
            elif op_code_resposta == OpCodes.CATEGORIA_NAO_EXISTE_PRODUTO:
                raise CategoriaNaoExiste(argumento)
            
            elif op_code_resposta in [OpCodes.PRECO_INVALIDO, OpCodes.NOVO_PRECO_INVALIDO]:
                raise PrecoInvalido()
            
            elif op_code_resposta == OpCodes.QUANTIDADE_INVALIDA:
                raise QuantidadeInvalida()
            
            elif op_code_resposta in [OpCodes.NOME_PRODUTO_INVALIDO, OpCodes.INCREMENTO_INVALIDO, OpCodes.NOME_CLIENTE_INVALIDO]:
                raise ValorArgumentoInvalido(argumento if argumento else "Valor de argumento inválido.")

            elif op_code_resposta in [OpCodes.CLIENTE_NAO_EXISTE, OpCodes.CLIENTE_NAO_EXISTE_REMOVE, OpCodes.CLIENTE_NAO_EXISTE_LISTA, OpCodes.CLIENTE_NAO_EXISTE_CHECKOUT, OpCodes.CLIENTE_NAO_EXISTE_ENCOMENDAS]:
                raise ClienteNaoExiste()
            
            elif op_code_resposta == OpCodes.EMAIL_JA_EXISTE:
                raise EmailJaExiste()
            
            elif op_code_resposta == OpCodes.EMAIL_INVALIDO:
                raise EmailInvalido()
            
            elif op_code_resposta == OpCodes.PASSWORD_INVALIDA:
                raise PasswordInvalida()

            elif op_code_resposta == OpCodes.QUANTIDADE_INVALIDA_CARRINHO:
                raise QuantidadeCarrinhoInvalida()
            
            elif op_code_resposta == OpCodes.STOCK_INSUFICIENTE:
                raise StockInsuficiente()
            
            elif op_code_resposta == OpCodes.PRODUTO_NAO_NO_CARRINHO:
                raise ProdutoNaoNoCarrinho()
            
            elif op_code_resposta == OpCodes.CARRINHO_VAZIO:
                raise CarrinhoVazio()
            
            elif op_code_resposta == OpCodes.FALHA_ENCOMENDA:
                raise FalhaEncomenda()

            else:
                raise ErroInterno(f"Erro recebido do servidor. Código: {op_code_resposta}. Detalhe: {argumento}")


        #Sucesso

        if comando == "CRIA_CATEGORIA":
            categoria = lista_resposta[0]
            return f"Categoria {categoria.nome} criada com sucesso."
            
        elif comando == "LISTA_CATEGORIAS":
            categorias = lista_resposta[0]
            produtos = lista_resposta[1]
            
            resultado = f"Total Categorias: {len(categorias)}\n"
            resultado += f"Total Produtos: {len(produtos)}\n\n"
            
            for categoria in categorias:
                quantidade_de_produtos = sum(1 for produto in produtos if produto.categoria == categoria.nome)
                resultado += f"{categoria.id_categoria}-{categoria.nome} ({quantidade_de_produtos} produtos);\n"

            return resultado.strip()

        elif comando == "REMOVE_CATEGORIA":
            return f"Categoria {argumentos[0]} removida com sucesso."

        elif comando == "CRIA_PRODUTO":
            produto = lista_resposta[0]
            return f"Produto {produto.nome} criado com sucesso."

        elif comando == "LISTA_PRODUTOS":
            categorias = lista_resposta[0] 
            produtos = lista_resposta[1]
            total_quantidade = sum(p.quantidade for p in produtos)
            
            resultado = f"Total Produtos: {len(produtos)}\n"
            resultado += f"Total Quantidade: {total_quantidade}\n\n"
            
            for produto in produtos:
                resultado += f"{produto.id_produto}-{produto.nome} ({produto.categoria}, {produto.preco:.2f} euros, {produto.quantidade} unidades);\n"
            return resultado.strip()

        elif comando == "AUMENTA_STOCK_PRODUTO":
            produto = lista_resposta[0]
            aumento = argumentos[1] 
            
            return f"Stock do produto {produto.nome} aumentado em {aumento} unidades com sucesso."

        elif comando == "ATUALIZA_PRECO_PRODUTO":
            produto = lista_resposta[0]
            novo_preco = float(argumentos[1])
            
            return f"O preço do produto {produto.nome} foi atualizado para {novo_preco:.2f} com sucesso."

        elif comando == "CRIA_CLIENTE":
            cliente = lista_resposta[0]
            
            return f"Cliente criado com sucesso com identificador único {cliente.id_cliente}."

        elif comando == "LISTA_CLIENTES":
            clientes = lista_resposta[0]
            resultado = f"Total Clientes: {len(clientes)}"
            
            for cliente in clientes:
                resultado += f"{cliente.id_cliente}- {cliente.nome} ({cliente.email});\n"
            return resultado.strip()

        elif comando == "ADICIONA_PRODUTO_CARRINHO":
            produto = lista_resposta[0]
            
            return f"Produto {produto.nome} adicionado com sucesso ao carrinho."

        elif comando == "REMOVE_PRODUTO_CARRINHO":
            produto = lista_resposta[0]
            
            return f"Produto {produto.nome} removido com sucesso do carrinho de compras."

        elif comando == "LISTA_CARRINHO":
            categorias = lista_resposta[0]
            produtos_carrinho = lista_resposta[1]
            
            quantidade_total = sum(produto.quantidade for produto in produtos_carrinho)
            preco_total = sum(produto.preco * produto.quantidade for produto in produtos_carrinho)
            
            resultado = f"Total Produtos: {len(produtos_carrinho)}\n"
            resultado += f"Total Quantidade: {quantidade_total}\n"
            resultado += f"Total Preço: {preco_total:.2f} euros\n\n"
            
            for produto in produtos_carrinho:
                categoria_id = next((categoria.id_categoria for categoria in categorias if categoria.nome == produto.categoria), "")
                resultado += f"{produto.id_produto}-{produto.nome} ({categoria_id}-{produto.categoria}, {produto.preco:.2f} euros, {produto.quantidade} unidades);\n"
            return resultado.strip()

        elif comando == "CHECKOUT_CARRINHO":
            return "Checkout de carrinho de compras efetuado com sucesso. Encomenda criada com sucesso a partir do carrinho."

        elif comando == "LISTA_ENCOMENDAS":
            encomendas = lista_resposta[0]
            produtos_por_encomenda = lista_resposta[1]

            if len(encomendas) == 0:
                return "Sem Encomendas"

            primeira_encomenda = encomendas[0]

            try:
                nome_cliente = primeira_encomenda.nome_cliente
                email_cliente = primeira_encomenda.email_cliente
            except AttributeError:
                nome_cliente = "Desconhecido"
                email_cliente = "sem@email.com"

            produtos_comprados = set()
            total_preco = 0.00 
            lista_categorias = {}

            resposta = ""

            for i in range(len(encomendas)):
                encomenda = encomendas[i]
                produtos_encomenda = produtos_por_encomenda[i]

                total_preco += encomenda.total_preco 

                total_produtos_encomenda = len(produtos_encomenda)
                total_quantidade_encomenda = 0

                resposta_produtos_desta_encomenda = ""

                for produto in produtos_encomenda:
                    produtos_comprados.add(produto.id_produto)
                    lista_categorias[produto.categoria] = lista_categorias.get(produto.categoria, 0) + produto.quantidade
                    total_quantidade_encomenda += produto.quantidade
                    
                    resposta_produtos_desta_encomenda += f"{produto.id_produto} - {produto.nome} ({produto.categoria}, {produto.preco:.2f} euros, {produto.quantidade} unidades);\n"

                resposta += f"ID Encomenda: {encomenda.id_encomenda}\n"
                resposta += f"Total Produtos: {total_produtos_encomenda}\n"
                resposta += f"Total Quantidade: {total_quantidade_encomenda}\n"
                resposta += f"Total Preço: {encomenda.total_preco:.2f} euros\n\n"
                resposta += resposta_produtos_desta_encomenda
                resposta += "\n"
                
            if lista_categorias:
                categoria_top = max(lista_categorias.values())
                categorias_empate = [categoria for categoria, quantidade in lista_categorias.items() if quantidade == categoria_top]
                categorias_empate.sort()
                categoria_top_frase = ", ".join(categorias_empate)
            else:
                categoria_top_frase = "N/A"

            total_preco = round(total_preco, 2)

            resposta_final = f"Cliente: {nome_cliente} {email_cliente}\n"
            resposta_final += f"Total Encomendas: {len(encomendas)}\n"
            resposta_final += f"Data Encomenda: {primeira_encomenda.data}\n" 
            resposta_final += f"Total Produtos: {len(produtos_comprados)}\n"
            resposta_final += f"Total Preço: {total_preco:.2f} euros\n"
            resposta_final += f"Categoria Top: {categoria_top_frase}\n\n"

            resposta_final += resposta

            return resposta_final.strip()
    
    def fechar_ligacao(self):
        self.stub.fechar_ligacao()