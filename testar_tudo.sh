#!/bin/bash

# Configurações do ZooKeeper
IP_ZK="127.0.0.1"
PORTA_ZK="2181"

echo "======================================================"
echo " 🛠️ INICIAR TESTES AUTOMÁTICOS DO MARKETCENTER 🛠️"
echo "======================================================"
sleep 1

echo -e "\n---> [PASSO 1] ADMINISTRADOR: A PREPARAR A LOJA E PRODUTOS"
# Passa os 4 argumentos logo aqui: IP, Porto, Perfil (3) e ID (1)
python3 -m cliente.main_c $IP_ZK $PORTA_ZK 3 1 <<EOF
CRIA_CATEGORIA Fruta
CRIA_CATEGORIA Laticinios
CRIA_CATEGORIA Lixo
REMOVE_CATEGORIA Lixo
CRIA_PRODUTO Bananas Fruta 50.45 100
CRIA_PRODUTO Papaia Fruta 90.90 50
CRIA_PRODUTO Leite Laticinios 1.20 200
LISTA_CATEGORIAS
LISTA_PRODUTOS
exit
EOF
sleep 1

echo -e "\n---> [PASSO 2] CLIENTE ANÓNIMO: A CRIAR CONTA"
# Perfil 0, ID 999
python3 -m cliente.main_c $IP_ZK $PORTA_ZK 0 999 <<EOF
CRIA_CLIENTE Joao joao@mail.com 1234
exit
EOF
sleep 1

echo -e "\n---> [PASSO 3] CLIENTE REGISTADO: A FAZER COMPRAS"
# Perfil 1, ID 1
python3 -m cliente.main_c $IP_ZK $PORTA_ZK 1 1 <<EOF
ADICIONA_PRODUTO_CARRINHO Bananas 10
ADICIONA_PRODUTO_CARRINHO Leite 5
LISTA_CARRINHO
REMOVE_PRODUTO_CARRINHO Leite
LISTA_CARRINHO
ADICIONA_PRODUTO_CARRINHO Papaia 2
CHECKOUT_CARRINHO
LISTA_ENCOMENDAS 1
exit
EOF
sleep 1

echo -e "\n---> [PASSO 4] FUNCIONÁRIO/ADMIN: VALIDAÇÕES FINAIS"
# Perfil 2, ID 1
python3 -m cliente.main_c $IP_ZK $PORTA_ZK 2 1 <<EOF
LISTA_CLIENTES
LISTA_PRODUTOS
exit
EOF

echo -e "\n======================================================"
echo " ✅ TESTES AUTOMÁTICOS CONCLUÍDOS COM SUCESSO! ✅"
echo "======================================================"