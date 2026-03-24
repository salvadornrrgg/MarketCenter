# -----------------------------
    #GRUPO 09    
    #Salvado Gonçalves   64162
    # Tomás Farinha      64253
    # Este ficheiro é a camada de transporte do cliente como se fosse um estafeta, aqui é onde se leva a mensagem de texto do cliente pela rede até ao servidor e trás a resposta de volta
# -----------------------------


import socket, struct
from shared.socket_utilities import PontoAcesso


class TCPSocketCliente:
    """
    Camada Transporte:
    - move strings 
    - não conhece regras de negócio
    - não interpreta comandos
    """

    def __init__(self, ponto_acesso):
        self.ponto_acesso = ponto_acesso
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ponto_acesso.endereco_ip, self.ponto_acesso.porto))

    # TODO: A completar
    def enviar_mensagem(self, pedido_bytes):
        size_bytes = struct.pack('!I', len(pedido_bytes))
        self.sock.sendall(size_bytes)
        self.sock.sendall(pedido_bytes)
        
    def receive_all(self, tamanho_desejado):
        dados_recebidos = bytearray()
        while len(dados_recebidos) < tamanho_desejado:
            bytes_em_falta = self.sock.recv(tamanho_desejado - len(dados_recebidos))    
            if not bytes_em_falta:
                raise Exception("A ligação foi encerrada inesperadamente.")        
            dados_recebidos.extend(bytes_em_falta)
    
        return bytes(dados_recebidos)
    
    
    def receber_resposta(self):
        size_bytes = self.receive_all(4)
        size = struct.unpack('!I', size_bytes)[0]
        resposta_bytes = self.receive_all(size)
        return resposta_bytes

    def fechar(self):
        self.sock.close()
