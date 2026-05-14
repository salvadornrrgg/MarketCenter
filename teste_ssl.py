import socket
import ssl
import struct
import pickle

def testar_ssl_manual():
    print("--- TESTE DE CONEXÃO SSL ---")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='root.pem') # Ajusta para .pem se necessário

    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Embrulhar o socket
    secure_sock = context.wrap_socket(raw_sock, server_hostname='127.0.0.1')
    
    try:
        secure_sock.connect(('127.0.0.1', 8888))
        print("✅ SUCESSO: Handshake SSL realizado com o servidor!")
        
        # Tentar um comando simples (ex: lista categorias)
        # [op_code, argumentos, id_perfil, id_user]
        pedido = [10200, [], 3, 1]
        p_bytes = pickle.dumps(pedido)
        secure_sock.sendall(struct.pack('!I', len(p_bytes)) + p_bytes)
        
        print("✅ SUCESSO: Dados enviados pelo túnel encriptado.")
        secure_sock.close()
    except Exception as e:
        print(f"❌ FALHA: Erro na ligação SSL: {e}")

if __name__ == "__main__":
    testar_ssl_manual()