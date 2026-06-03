# MarketCenter - Aplicações Distribuídas (Fase 3)

**Grupo 09**
* Salvador Gonçalves (64162)
* Tomás Farinha (64253)

---

## Descrição do Projeto
O MarketCenter é uma aplicação distribuída de comércio eletrónico baseada numa arquitetura cliente-servidor com recurso a *Remote Procedure Calls* (RPC). 

A Fase 3 do projeto foca-se na evolução da arquitetura base para um sistema de alta disponibilidade, introduzindo comunicação segura, coordenação distribuída e tolerância a falhas através do modelo Chain Replication.

---

## Implementações da Fase 3

### 1. Segurança e Encriptação (SSL/TLS)

Todas as comunicações entre o Cliente e o Servidor são feitas através de túneis encriptados utilizando o protocolo TLS
Testamos se estava tudo certo com o ficheiro "teste_ssl.py"

- Usamos Autenticação Unilateral. O cliente verifica a identidade do servidor antes de enviar qualquer dado.
- Camada de Rede:** A segurança está abstraída nas classes `TCPSocketServidor` e `TCPSocketCliente`, que envolvem os sockets convencionais num `ssl.SSLContext`.
- Certificados (OpenSSL):**
- `root.pem` / `root.key`: Autoridade Certificadora (CA) criada localmente.
- `serv.crt` / `serv.key`: Certificado e chave privada do servidor, assinados pela CA local. O servidor utiliza o _Common Name_ `localhost`.
- `cli.crt` / `cli.key`: Não foram usadas mas deixamos estar, Certificado e chave privada do cliente, assinados pela CA local. O cliente utiliza o _Common Name_ `localhost`.

### 2. Coordenação Distribuída (ZooKeeper)

- Utilização da biblioteca kazoo para gestão de nós no ZooKeeper.
- Descoberta de Serviços: Os servidores criam nós efémeros (ex: node0000000000) na diretoria /chain, publicando o seu IP e Porto.
- Watchers: O cliente possui um "olheiro" (zookeeperCliente.py) que é notificado em tempo real sempre que a cadeia muda, atualizando automaticamente as ligações à Head e à Tail sem interromper o utilizador.

### 3. Tolerância a Falhas e Replicação (Chain Replication)

- Separação de fluxos: O cliente envia operações de escrita para a Head (cabeça da cadeia) e operações de leitura para a Tail (cauda da cadeia).
- Encaminhamento RPC: A Head atualiza a base de dados (Loja) e reencaminha a operação de escrita para o seu sucessor, até chegar à Tail, que responde ao cliente.
- Sincronização de Estado: Quando um novo servidor entra na rede, ele liga-se ao seu antecessor para pedir a sincronização total e automática do estado da Loja antes de começar a aceitar pedidos.

### 4. Arquitetura RPC Robusta (Herdada da Fase 2)

- Tratamento dinâmico de múltiplos clientes em simultâneo através da multiplexação de I/O (select()).
- Serialização de objetos nativos com pickle.
- Prevenção de fragmentação de pacotes na rede através da leitura baseada no tamanho do cabeçalho.
- Proteção rigorosa de inputs (Validação estrita de tipos para evitar falhas críticas no servidor e gestão de try/except para prevenir crashes).

Escolhas de Implementação 

Autenticação Interativa vs. CLI: 
O enunciado da Fase 3 especifica que o cliente deve ser iniciado apenas com o IP e Porto do ZooKeeper.
No entanto, a lógica de negócio (Fase 2) exige o ID de Utilizador e Perfil para validar permissões. 
Decisão: Optámos por manter os argumentos da CLI mínimos (conforme Fase 3) e introduzir um menu de login interativo no arranque do programa.
Isto garante que o sistema é seguro e que as permissões de Administrador/Cliente são respeitadas sem violar os requisitos de arranque da Fase 3.

Gestão de IPs (Bind vs. Anúncio):
Para cumprir o requisito de avaliação que penaliza o uso de localhost no ZooKeeper, o servidor executa o bind do socket em 0.0.0.0 (escutando em todas as interfaces), 
mas anuncia o seu IP Real (obtido via interface de rede ativa) ao ZooKeeper. 

Encadeamento Seguro:
A comunicação segura (TLS) não foi aplicada apenas ao cliente. Todas as ligações internas da Chain Replication (sincronização de estado entre servidores e reencaminhamento de escritas) 
utilizam igualmente sockets SSL, garantindo que nenhum dado circula em texto limpo dentro do sistema distribuído.

Recuperação Automática de Ligações: 
O Stub do cliente foi desenhado para ser resiliente. Sempre que o ZooKeeper deteta uma falha na Head ou Tail, o Stub reconstrói os objetos de rede automaticamente sem que o utilizador precise de reiniciar o cliente ou reintroduzir comandos.

Criamos o script "testar_tudo.sh" para correr todos os comandos e funcionalidades 

## Como Preparar o Ambiente (Antes de Correr)

  1. Ativar o Ambiente Virtual:
A biblioteca kazoo deve estar instalada no ambiente virtual.  execute primeiro:
    source vvv/bin/activate

  2. Garantir os Certificados:
Os certificados root.pem, serv.crt e serv.key devem estar gerados e presentes na raiz do projeto.

  3. Iniciar e Limpar o ZooKeeper:
Garanta que o serviço do ZooKeeper está a correr. Se for testar de raiz, limpe a cadeia de execuções anteriores:
Abra o cliente do ZK: ./zkCli.sh
Execute o comando: deleteall /chain
Saia com quit


## Como Executar

  1. Iniciar os Servidores 
O servidor necessita de saber a sua própria porta e onde encontrar o ZooKeeper. 
Deve arrancar pelo menos um servidor, mas recomendamos três para observar a Chain Replication.
A partir da raiz do projeto, abra terminais separados e execute:

  Servidor 1 (Head):
          python3 -m servidor.main 5000 127.0.0.1 2181
  
  Servidor 2 (Intermédio):
          python3 -m servidor.main 5001 127.0.0.1 2181
        
  Servidor 3 (Tail):
          python3 -m servidor.main 5002 127.0.0.1 2181

   2. Iniciar o Cliente
Num terminal separado, arranque o cliente indicando apenas o IP e o Porto do ZooKeeper (como exigido no guião da Fase 3).
O nosso cliente solicitará os dados de autenticação de forma interativa e elegante!

          python3 -m cliente.main_c 127.0.0.1 2181

Logo após o arranque, escolha o Perfil (0 a 3) e um ID de utilizador para poder gerir permissões.
(Ex: Perfil 3 para o Administrador criar a Loja, e depois um novo cliente com Perfil 1 para fazer compras). Para encerrar qualquer cliente e limpar os sockets em segurança, digite exit.
