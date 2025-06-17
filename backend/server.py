# backend/server.py
import socket, threading

# Lista pra armazenar os clientes conectados
#clients = []
#usernames = []

clients = {}

def handle_client(client_socket):
    try:
        # Recebe usuário
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        
        print(f"[+] {username} entrou no chat.")
        
        # Avisa os outros usuários que alguém novo entrou
        broadcast(f"🔔 {username} entrou no chat!", client_socket)
        
        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"[{clients[client_socket]}]: {msg}")
            broadcast(f"{clients[client_socket]}: {msg}", client_socket)
    except Exception as e:
        print(f"[X] Erro com cliente: {e}")
    
    finally:
        # Remove o cliente da lista
        if client_socket in clients:
            username = clients.pop(client_socket)
            print(f"[-] {username} saiu do chat.")
            client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Remove o cliente bugado
                username = clients.pop(client, 'desconhecido')
                print(f"[ERRO AO ENVIAR]: {username}")
                client.close()

# Iniciar o server
def start_server(host= '0.0.0.0', port=8080):
    #SOCK_STREAM = TCP e AF_INET = IPv4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Liga o socket ao endereço e porta
    server.bind((host, port))
    server.listen()
    print(f"🚀 Servidor de chat rodando em {host}:{port}")
    
    while True:
        # Aceita conexões
        client_socket, addr = server.accept()
        print(f"[+] Nova conexão de {addr}")
        
        # Criação de thread para o cliente
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
