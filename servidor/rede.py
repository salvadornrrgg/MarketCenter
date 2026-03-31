# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    #Neste ficheiro recebe se o pedido do cliente e lê se o texto, ele entrega o pedido ao processador.py, ele pega na resposta final do processador e devolve pela rede ao cliente
# -----------------------------


import socket, sys, struct
import select as sel
from shared.socket_utilities import PontoAcesso

class TCPSocketServidor:
    """
    Camada Transporte:
    - não interpreta comandos
    - não chama Loja
    - não faz validações de negócio
    - só move strings
    """

    def __init__(self, ponto_acesso):
        self.ponto_acesso = ponto_acesso
        self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_server.bind((self.ponto_acesso.endereco_ip, self.ponto_acesso.porto))
        self.sock_server.listen(5)
        self.socket_list = [self.sock_server, sys.stdin] 
        self.a_correr = True

    def receive_all(self, conn_sock, tamanho_desejado):
        dados_recebidos = bytearray()
        while len(dados_recebidos) < tamanho_desejado:
            bytes_em_falta = conn_sock.recv(tamanho_desejado - len(dados_recebidos))    
            if not bytes_em_falta:
                return None       
            dados_recebidos.extend(bytes_em_falta)

        return bytes(dados_recebidos)
    
    def receber_pedido(self, conn_sock):
        size_bytes = self.receive_all(conn_sock, 4)
        if not size_bytes:
            return None
            
        size = struct.unpack('!I', size_bytes)[0]
        pedido_bytes = self.receive_all(conn_sock, size)
        return pedido_bytes

    def enviar_resposta(self, conn_sock, resposta_bytes):
        size_bytes = struct.pack('!I', len(resposta_bytes))
        conn_sock.sendall(size_bytes)
        conn_sock.sendall(resposta_bytes)

    def aceitar(self, processa_pedido):
        while self.a_correr:
            R, W, X = sel.select(self.socket_list, [], [])

            for sock in R:
                if sock is sys.stdin:
                    comando = sys.stdin.readline().strip().lower()
                    if comando in ['exit', 'quit']:
                        self.a_correr = False
                        print ("SERVIDOR> A encerrar o servidor de forma controlada...")
                        self.fechar_tudo()
                        break
                elif sock is self.sock_server:
                    (conn_sock, addr) = self.sock_server.accept()
                    ip, port = conn_sock.getpeername()
                    print('Novo cliente ligado desde %s:%d' % (ip, port))
                    self.socket_list.append(conn_sock)
                else:
                    try:
                        pedido_bytes = self.receber_pedido(sock)
                        if pedido_bytes is None:
                            print(f"SERVIDOR> Cliente {sock.getpeername()} desligou-se.")
                            self.socket_list.remove(sock)
                            sock.close()
                        else:
                            resposta_bytes = processa_pedido(pedido_bytes)
                            self.enviar_resposta(sock, resposta_bytes)
                    except Exception as e:
                        print(f"SERVIDOR> Erro na ligação com o cliente: {e}")
                        if sock in self.socket_list:
                            self.socket_list.remove(sock)
                        sock.close()


    def fechar_tudo(self):
        for socket in self.socket_list:
            if socket is not sys.stdin:
                socket.close()