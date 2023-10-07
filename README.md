# Chat TCP em Python

Este é um simples sistema de chat cliente-servidor implementado em Python usando TCP. Ele suporta múltiplos clientes e possui comandos específicos que os usuários podem enviar para interagir com o servidor e outros clientes.

## Como usar

### Requisitos

- Python 3.x

### Executando o Servidor

1. Abra um terminal.
2. Navegue até o diretório onde os arquivos `server.py` e `client.py` estão localizados.

```bash
  cd caminho/do/seu/projeto
```

1. Execute o servidor.

```bash
  python server.py
```

O servidor será iniciado e começará a aguardar conexões de clientes.

### Executando o Cliente

1. Abra um novo terminal.
2. Navegue até o mesmo diretório onde os arquivos `server.py` e `client.py` estão localizados.

```bash
  cd caminho/do/seu/projeto
```

1. Execute o cliente.

```bash
  python client.py
```

1. O cliente solicitará que você insira o IP do servidor, a porta e um apelido.

2. Após entrar no chat, você pode enviar mensagens simplesmente digitando no terminal.

## Comandos do Cliente

- `/ENTRAR <IP> <PORTA> <APELIDO>`: Conecta o cliente ao servidor com o endereço IP, porta e apelido fornecidos.
- `/USUARIOS`: Lista os usuários atualmente conectados ao chat.
- `/NICK <NOVO_APELIDO>`: Altera o apelido do cliente para o novo apelido especificado.
- `/SAIR`: Desconecta o cliente do chat.

## Notas Importantes

- A sala do chat suporta no máximo 4 pessoas conectadas.
- O servidor e os clientes devem ser executados em terminais separados.

## Exemplo de Uso

1. Execute o servidor em um terminal.
2. Execute vários clientes em terminais separados.
3. Os clientes se conectam ao servidor usando o comando `/ENTRAR` e interagem com o chat usando os comandos mencionados.

## `server.py` - Servidor

1. Importação de bibliotecas: O código começa importando a biblioteca `socket` para usar as funcionalidades de comunicação por soquete e `threading` para lidar com várias conexões em threads separadas.

2. Variáveis Globais: Define algumas variáveis globais, como `clientes` para rastrear os clientes conectados e `MAX_CLIENTES` para o número máximo de clientes suportados na sala.

3. Função `handle_client`: Esta função é executada em uma thread separada para cada cliente conectado. Ela lê os comandos enviados pelo cliente, como `/ENTRAR`, `/USUARIOS`, `/NICK` e `/SAIR`, e executa ações correspondentes.

4. Funções de Comando: Existem funções específicas para cada comando, como `entrar_no_chat`, `listar_usuarios`, `mudar_apelido` e `sair_do_chat`. Essas funções processam os comandos do cliente e atualizam a lista de clientes conectados, enviam mensagens de broadcast ou fazem outras ações necessárias.

5. Função `broadcast`: Essa função envia uma mensagem para todos os clientes conectados, exceto o cliente que a enviou.

6. Função `encaminhar_mensagem`: Essa função envia uma mensagem de um cliente para todos os outros clientes na sala de chat.

7. Função `main`: A função principal do servidor configura o soquete do servidor, vincula-o a um endereço IP e porta específicos e fica ouvindo por conexões de clientes em um loop infinito. Quando um cliente se conecta, um novo thread é criado para lidar com esse cliente usando a função `handle_client`.

## `client.py` - Cliente

1. Função `receive_messages`: Esta função é executada em uma thread separada e é responsável por receber e exibir mensagens enviadas pelo servidor.

2. Função `main`: A função principal do cliente solicita ao usuário que insira o IP do servidor, a porta e um apelido. Ela então tenta se conectar ao servidor. Após a conexão bem-sucedida, inicia uma thread para receber mensagens do servidor.

3. Comandos do Cliente: O cliente aguarda comandos do usuário, como mensagens de texto ou comandos especiais, como `/SAIR`. Quando o usuário envia uma mensagem, ela é enviada ao servidor para ser encaminhada para outros clientes.

Resumidamente, o servidor cria um soquete para aceitar conexões de clientes e gerencia as interações entre eles, enquanto o cliente cria um soquete para se conectar ao servidor e permite que os usuários enviem comandos e mensagens. As threads são usadas para permitir que várias conexões e a comunicação ocorram simultaneamente.
