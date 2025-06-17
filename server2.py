import socket  # Biblioteca padrão pra criar comunicação entre computadores
import threading  # Pra rodar cada cliente em uma thread separada (paralelismo leve)

# Listas globais pra guardar os sockets e nomes dos usuários conectados
clients = []
usernames = []

# Essa função vai rodar em uma thread separada pra cada cliente conectado
def handle_client(client_socket):
    try:
        # Primeiro, recebe o nome do usuário
        username = client_socket.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client_socket)

        print(f"[+] {username} entrou no chat.")

        # Avisa os outros usuários que alguém novo entrou
        broadcast(f"🔔 {username} entrou no chat!", client_socket)

        # Fica escutando novas mensagens desse cliente enquanto ele estiver online
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break  # Cliente caiu ou fechou a conexão
            print(f"[{username}]: {msg}")
            broadcast(f"{username}: {msg}", client_socket)

    except Exception as e:
        print(f"[x] Erro com cliente: {e}")

    finally:
        # Se o cliente sair, remove ele das listas e avisa os outros
        if client_socket in clients:
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            username = usernames.pop(index)
            broadcast(f"❌ {username} saiu do chat.", None)

# Essa função envia a mensagem pra todos os clientes conectados (menos o remetente, se quiser)
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass  # Se der erro (ex: cliente desconectado), ignora e segue o baile

# Função principal que inicia o servidor
def start_server(host='0.0.0.0', port=8080):
    # Cria um socket TCP (SOCK_STREAM) usando IPv4 (AF_INET)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket ao endereço e porta
    server.bind((host, port))

    # Começa a escutar por conexões (sem limite definido de backlog aqui)
    server.listen()

    print(f"🚀 Servidor de chat rodando em {host}:{port}")

    # Loop infinito que aceita novos clientes
    while True:
        # Espera (bloqueia) até que um novo cliente conecte
        client_socket, addr = server.accept()
        print(f"[+] Nova conexão de {addr}")

        # Cria uma nova thread só pra esse cliente
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

# Execução direta do script
if __name__ == "__main__":
    start_server()
