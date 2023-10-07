import socket
import threading

# Dicionário para armazenar clientes conectados e seus apelidos
clients = {}

# Máximo de clientes na sala
MAX_CLIENTS = 4

def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Analisar os comandos do cliente
            if data.startswith('/ENTRAR'):
                _, ip, porta, nickname = data.split()
                join_chat(client_socket, client_address, nickname)
            elif data.startswith('/USUARIOS'):
                list_users(client_socket)
            elif data.startswith('/NICK'):
                _, new_nickname = data.split()
                change_nickname(client_socket, new_nickname)
            elif data.startswith('/SAIR'):
                break
            else:
                forward_message(client_socket, data)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if nickname:
            leave_chat(client_socket, nickname)

def join_chat(client_socket, client_address, nickname):
    if len(clients) < MAX_CLIENTS and nickname not in clients.values():
        clients[client_socket] = nickname
        broadcast(f"{nickname} entrou no chat.")
        print(f"{nickname} ({client_address}) entrou no chat.")
    else:
        client_socket.send("Limite de clientes atingido ou apelido já em uso. Conexão negada.".encode('utf-8'))
        client_socket.close()

def list_users(client_socket):
    users = ', '.join(clients.values())
    client_socket.send(f"Usuários conectados: {users}".encode('utf-8'))

def change_nickname(client_socket, new_nickname):
    current_nickname = clients[client_socket]
    if new_nickname not in clients.values():
        clients[client_socket] = new_nickname
        broadcast(f"{current_nickname} mudou o apelido para {new_nickname}.")
    else:
        client_socket.send("Apelido já em uso.".encode('utf-8'))

def leave_chat(client_socket, apelido):
    if client_socket in clients:
        del clients[client_socket]
        broadcast(f"{apelido} saiu do chat.")
        print(f"{apelido} saiu do chat.")
    client_socket.close()

def broadcast(message, sender_socket=None):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                continue
        elif sender_socket is None:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                continue
                

def forward_message(client_socket, message):
    apelido = clients[client_socket]
    broadcast(f"{apelido}: {message}", client_socket)

def main():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Servidor ouvindo em {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    main()
