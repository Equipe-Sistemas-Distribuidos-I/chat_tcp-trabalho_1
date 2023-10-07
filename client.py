import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            break

def main():
    while True:
        input_command = input("Digite '/ENTRAR' para entrar no chat, '/SAIR' para sair: ")

        if input_command == '/ENTRAR':
            host = input("Digite o IP do servidor: ")
            port = int(input("Digite a porta do servidor: "))
            nickname = input("Digite seu apelido: ")

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            join_command = f"{input_command} {host} {port} {nickname}"
            client_socket.send(join_command.encode('utf-8'))

            # Receber resposta do servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(response)

            if "Conexão negada" not in response:
                break
        elif input_command == '/SAIR':
            print("Saindo do chat.")
            return
        else:
            print("Comando inválido. Tente novamente.")

    # Thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message == "/SAIR":
            client_socket.send(message.encode('utf-8'))
            break
        else:
            client_socket.send(message.encode('utf-8'))

    client_socket.close()

if __name__ == "__main__":
    main()
