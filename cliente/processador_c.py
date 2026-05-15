# -----------------------------
# GRUPO 09    
# Salvador Gonçalves   64162
# Tomás Farinha        64253
# -----------------------------

from cliente.stub import Stub
import shlex
from shared.socket_utilities import PontoAcesso
from shared.excepcoes import OpCodes, ExcepcaoBase

class Processador:

    def __init__(self, hosts_zk, id_perfil, id_user):
        self.stub = Stub(hosts_zk)
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
            
        comando_str = pedido_partido[0].upper()
        argumentos = pedido_partido[1:]

        if comando_str not in self.codigos_operacoes:
            return f"Erro: O comando {comando_str} não é conhecido."

        op_code = self.codigos_operacoes[comando_str]

        try:
            if comando_str == "CRIA_PRODUTO":
                argumentos[2] = float(argumentos[2]) 
                argumentos[3] = int(argumentos[3])   
            elif comando_str == "AUMENTA_STOCK_PRODUTO":
                argumentos[1] = int(argumentos[1])
            elif comando_str == "ATUALIZA_PRECO_PRODUTO":
                argumentos[1] = float(argumentos[1])
            elif comando_str == "ADICIONA_PRODUTO_CARRINHO":
                argumentos[1] = int(argumentos[1])
        except ValueError:
            return "Erro no cliente: Escreveste texto onde devia estar um número!"
        
        pedido_em_lista = [op_code, argumentos, self.idPerfil, self.id_user]
        print(f"Pedido: {pedido_em_lista}")

        resposta = self.stub.processa(pedido_em_lista)
        op_code_resposta = resposta[0]
        lista_resposta = resposta[1]

        if op_code_resposta >= 30000:
            msg_erro = lista_resposta[0] if lista_resposta else "Erro desconhecido no servidor."
            
            raise ExcepcaoBase(msg_erro, op_code_resposta)

        

        if comando_str == "CRIA_CATEGORIA":
            categoria = lista_resposta[0]
            return f"Categoria {categoria.nome} criada com sucesso."
            
        elif comando_str == "LISTA_CATEGORIAS":
            categorias = lista_resposta[0]
            produtos = lista_resposta[1]
            
            res = f"Total Categorias: {len(categorias)}\nTotal Produtos: {len(produtos)}\n\n"
            for cat in categorias:
                qtd = sum(1 for p in produtos if p.categoria == cat.nome)
                res += f"{cat.id_categoria}-{cat.nome} ({qtd} produtos);\n"
            return res.strip()

        elif comando_str == "REMOVE_CATEGORIA":
            return f"Categoria {argumentos[0]} removida com sucesso."

        elif comando_str == "CRIA_PRODUTO":
            produto = lista_resposta[0]
            return f"Produto {produto.nome} criado com sucesso."

        elif comando_str == "LISTA_PRODUTOS":
            produtos = list(lista_resposta[1].values()) if isinstance(lista_resposta[1], dict) else lista_resposta[1]
            total_stock = sum(p.quantidade for p in produtos)
            
            res = f"Total Produtos: {len(produtos)}\nTotal Quantidade: {total_stock}\n\n"
            for p in produtos:
                res += f"{p.id_produto}-{p.nome} ({p.categoria}, {p.preco:.2f} euros, {p.quantidade} unidades);\n"
            return res.strip()

        elif comando_str == "AUMENTA_STOCK_PRODUTO":
            produto = lista_resposta[0]
            return f"Stock do produto {produto.nome} aumentado com sucesso. Stock atual: {produto.quantidade}."

        elif comando_str == "ATUALIZA_PRECO_PRODUTO":
            produto = lista_resposta[0]
            return f"Preço do produto {produto.nome} atualizado para {produto.preco:.2f} euros."

        elif comando_str == "CRIA_CLIENTE":
            cliente = lista_resposta[0]
            return f"Cliente criado com sucesso com identificador único {cliente.id_cliente}."

        elif comando_str == "LISTA_CLIENTES":
            clientes = list(lista_resposta[0].values()) if isinstance(lista_resposta[0], dict) else lista_resposta[0]
            res = f"Total Clientes: {len(clientes)}\n"
            for cli in clientes:
                res += f"{cli.id_cliente}- {cli.nome} ({cli.email});\n"
            return res.strip()

        elif comando_str == "ADICIONA_PRODUTO_CARRINHO":
            produto = lista_resposta[0]
            return f"Produto {produto.nome} adicionado com sucesso ao carrinho."

        elif comando_str == "REMOVE_PRODUTO_CARRINHO":
            produto = lista_resposta[0]
            return f"Produto {produto.nome} removido do carrinho com sucesso."

        elif comando_str == "LISTA_CARRINHO":
            produtos_no_carrinho = lista_resposta[1]

            if not produtos_no_carrinho:
                return "O teu carrinho está vazio."

            resultado = "--- PRODUTOS NO TEU CARRINHO ---\n"
            total_carrinho = 0
            
            for p in produtos_no_carrinho:
                subtotal = p.preco * p.quantidade
                total_carrinho += subtotal
                
                resultado += f"ID: {p.id_produto} | {p.nome} ({p.categoria})\n"
                resultado += f"   Quant: {p.quantidade} x {p.preco:.2f}€ = {subtotal:.2f}€\n"
                resultado += "--------------------------------\n"

            resultado += f"TOTAL A PAGAR: {total_carrinho:.2f} euros"
            return resultado
        elif comando_str == "CHECKOUT_CARRINHO":
            encomenda = lista_resposta[0]
            return f"Checkout efetuado com sucesso. Encomenda #{encomenda.id_encomenda} gerada."

        elif comando_str == "LISTA_ENCOMENDAS":
            encomendas = lista_resposta[0]
            if not encomendas:
                return "Sem encomendas registadas para este utilizador."
            
            total_gasto = sum(e.total_preco for e in encomendas)
            res = f"Total Encomendas: {len(encomendas)}\nTotal Gasto: {total_gasto:.2f} euros\n"
            res += "--------------------------------------\n"
            for e in encomendas:
                res += f"Enc #{e.id_encomenda} | Data: {e.data} | Total: {e.total_preco:.2f}€\n"
            return res.strip()

        return "Operação realizada com sucesso."

    def fechar_ligacao(self):
        self.stub.fechar_ligacao()