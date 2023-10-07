import socket
import threading

# Dicionário para armazenar clientes conectados e seus apelidos
clientes = {}

# Máximo de clientes na sala
MAX_CLIENTES = 4

def handle_client(client_socket, client_address):
    apelido = None

    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Analisar os comandos do cliente
            if data.startswith('/ENTRAR'):
                _, ip, porta, apelido = data.split()
                entrar_no_chat(client_socket, client_address, apelido)
            elif data.startswith('/USUARIOS'):
                listar_usuarios(client_socket)
            elif data.startswith('/NICK'):
                _, novo_apelido = data.split()
                mudar_apelido(client_socket, novo_apelido)
            elif data.startswith('/SAIR'):
                break
            else:
                encaminhar_mensagem(client_socket, data)

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        if apelido:
            sair_do_chat(client_socket, apelido)

def entrar_no_chat(client_socket, client_address, apelido):
    if len(clientes) < MAX_CLIENTES and apelido not in clientes.values():
        clientes[client_socket] = apelido
        broadcast(f"{apelido} entrou no chat.")
        print(f"{apelido} ({client_address}) entrou no chat.")
    else:
        client_socket.send("Limite de clientes atingido ou apelido já em uso. Conexão negada.".encode('utf-8'))
        client_socket.close()

def listar_usuarios(client_socket):
    usuarios = ', '.join(clientes.values())
    client_socket.send(f"Usuários conectados: {usuarios}".encode('utf-8'))

def mudar_apelido(client_socket, novo_apelido):
    apelido_atual = clientes[client_socket]
    if novo_apelido not in clientes.values():
        clientes[client_socket] = novo_apelido
        broadcast(f"{apelido_atual} mudou o apelido para {novo_apelido}.")
    else:
        client_socket.send("Apelido já em uso.".encode('utf-8'))

def sair_do_chat(client_socket, apelido):
    if client_socket in clientes:
        del clientes[client_socket]
        broadcast(f"{apelido} saiu do chat.")
        print(f"{apelido} saiu do chat.")
    client_socket.close()

def broadcast(message, sender_socket=None):
    for client_socket in clientes:
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
                

def encaminhar_mensagem(client_socket, message):
    apelido = clientes[client_socket]
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
