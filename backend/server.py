# backend/server.py
import socket, threading

# Lista pra armazenar os clientes conectados
#clients = []
#usernames = []

clients = {}

rooms = {
    "geral": set(),
    "games": set(),
    "estudos": set(),
}

def handle_client(client_socket):
    try:
        # Recebe usuário
        username = client_socket.recv(1024).decode('utf-8')
        
        # Se não mandou nome, desconecta sem log
        if not username:
            client_socket.close()
            return
        
        clients[client_socket] = username
        rooms.setdefault("geral", set()).add(client_socket)  # Adiciona o socket na sala 'geral'
        
        print(f"[+] {username} entrou no chat.")
        
        # Avisa os outros usuários que alguém novo entrou
        broadcast(f"🔔 {username} entrou no chat!", client_socket)
        
        while True:
            
            msg = client_socket.recv(1024).decode('utf-8')
            
            # Mensagem privada
            if msg.startswith('/msg '):
                parts = msg.split(' ', 2)
                destinatario = parts[1]
                conteudo = parts[2]
                for sock, nome in clients.items():
                    if nome == destinatario:
                        sock.send(f"[PRIVADO] {clients[client_socket]}: {conteudo}".encode('utf-8'))
                        break
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

def broadcast(message, sender_socket, sala="geral"):
    for client in rooms[sala]:

        try:
            client.send(message.encode('utf-8'))
        except:
            # Remove o cliente bugado
            username = clients.pop(client, 'desconhecido')
            print(f"[ERRO AO ENVIAR]: {username}")
            client.close()

# Iniciar o server
def start_server(host='0.0.0.0', port=4242):
    #SOCK_STREAM = TCP e AF_INET = IPv4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite reusar a porta logo após fechar

    # Liga o socket ao endereço e porta
    server.bind((host, port))
    server.listen()
    print(f"🚀 Servidor de chat rodando em {host}:{port}")
    
    while True:
        # Aceita conexões
        client_socket, addr = server.accept()
        # print(f"[+] Nova conexão de {addr}")
        
        # Criação de thread para o cliente
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
