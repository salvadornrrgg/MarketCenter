# MarketCenter - Aplicações Distribuídas (Fase 3)

**Grupo 09**
* Salvador Gonçalves (64162)
* Tomás Farinha (64253)

---

## Descrição do Projeto
O MarketCenter é uma aplicação distribuída de comércio eletrónico baseada numa arquitetura cliente-servidor com recurso a *Remote Procedure Calls* (RPC). 

A Fase 3 do projeto foca-se na evolução da arquitetura base para um sistema de alta disponibilidade, introduzindo comunicação segura, coordenação distribuída e tolerância a falhas.

---

## Implementações da Fase 3

### 1. Segurança e Encriptação (SSL/TLS)
Todas as comunicações entre o Cliente e o Servidor são feitas através de túneis encriptados utilizando o protocolo TLS
Testamos se estava tudo certo com o ficheiro teste_ssl.py

* **Usamos Autenticação Unilateral. O cliente verifica a identidade do servidor antes de enviar qualquer dado.
* **Camada de Rede:** A segurança está abstraída nas classes `TCPSocketServidor` e `TCPSocketCliente` (`rede.py` e `rede_c.py`), que envolvem os sockets convencionais num `ssl.SSLContext`.
* **Certificados (OpenSSL):**
  * `root.pem` / `root.key`: Autoridade Certificadora (CA) criada localmente.
  * `serv.crt` / `serv.key`: Certificado e chave privada do servidor, assinados pela CA local. O servidor utiliza o _Common Name_ `localhost`.

### 2. Arquitetura RPC Robusta (Herdada da Fase 2)
* Tratamento dinâmico de múltiplos clientes em simultâneo através da multiplexação de I/O (`select()`).
* Serialização de objetos nativos com `pickle`.
* Prevenção de fragmentação de pacotes na rede através da leitura baseada no tamanho do cabeçalho (*Network Byte Order*).
* Proteção rigorosa de *inputs* (Validação estrita de *strings* e *inteiros* para evitar falhas críticas no servidor).







## Como Executar (Versão com SSL)

**1. Requisitos Prévios:**
Garantir que os certificados `root.pem`, `serv.crt` e `serv.key` estão gerados e presentes na raiz do projeto.

**2. Iniciar o Servidor:**
A partir da raiz do projeto, executar:
    python3 -m servidor.main

**3. Iniciar o Cliente:
Num terminal separado, executar:
    python3 -m cliente.main