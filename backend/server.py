import socket, threading
import json
import time

# Lista pra armazenar os clientes conectados
#clients = []
#usernames = []

clients = {}
usernames = {}

rooms = {
    "geral": set(),
    "games": set(),
    "estudos": set(),
}

# --- Funções de Banco de Dados (Stubs) ---
# No futuro, estas funções irão interagir com seu banco de dados (SQLite, PostgreSQL, etc.)

def save_message_to_db(message_data):
    """Salva uma mensagem no banco de dados. (Implementação futura)"""
    # Exemplo: INSERT INTO messages (sender, target, content, type, room) VALUES (...)
    # print(f"[DB STUB] Salvando: {message_data}")
    pass

def load_message_history(room_or_user_pair):
    """Carrega o histórico de mensagens para uma sala ou chat privado. (Implementação futura)"""
    # Exemplo: SELECT * FROM messages WHERE room = ? OR (sender = ? AND target = ?) ...
    # print(f"[DB STUB] Carregando histórico para: {room_or_user_pair}")
    return []

# --- Funções de Rede ---

def broadcast(message_data, sockets_to_send):
    """Envia uma mensagem JSON para uma lista específica de sockets."""
    message_json = json.dumps(message_data)
    for client_socket in list(sockets_to_send):
        try:
            client_socket.send(message_json.encode('utf-8'))
        except:
            # Se falhar, remove o cliente problemático
            remove_client(client_socket)
            
def remove_client(client_socket):
    """Remove um cliente de todas as estruturas de dados e notifica os outros."""
    if client_socket in clients:
        username = clients.pop(client_socket)
        usernames.pop(username, None)
        print(f"[-] {username} desconectado.")
        
        # Remove o cliente de todas as salas
        for room in rooms.values():
            room.discard(client_socket)
            
        # Notifica a saída do usuário
        notification = {
            "type": "user_left",
            "timestamp": time.time(),
            "username": username
        }
        broadcast(notification, clients.keys()) # Envia para todos que sobraram
        
# --- Lógica Principal do Cliente ---

def handle_client(client_socket):
    username = None
    try:
        # 1. Espera pelo nome de usuario
        username = client_socket.recv(1024).decode('utf-8').strip()

        # 2. Valida nome de usuário
        if not username or username in usernames:
            print(f"[!] Conexão recusada: username '{username}' é inválido ou já está em uso.")
            client_socket.close()
            return
            
        # 3. Registra usuario
        clients[client_socket] = username
        usernames[username] = client_socket
        rooms["geral"].add(client_socket)
        
        print(f"[+] {username} se registrou e entrou no chat.")

        # Notifica a todos sobre a entrada do novo usuário
        join_notification = {"type": "user_joined", "timestamp": time.time(), "username": username}
        broadcast(join_notification, clients.keys())

        # Envia a lista de usuários para o cliente que acabou de entrar
        user_list_update = {"type": "user_list", "users": list(usernames.keys())}
        client_socket.send(json.dumps(user_list_update).encode('utf-8'))
        
        # 4. Loop de Mensagens
        while True:
            
            msg_content = client_socket.recv(1024).decode('utf-8').strip()
            
            if not msg_content:
                break
            
            # 4.1. Tratamento de Comandos
            if msg_content.startswith('/priv '):
                parts = msg_content.split(' ', 2)
                if len(parts) < 3:
                    continue # Ignora comando malformado
                
                target_user = parts[1]
                content = parts[2]
                
                if target_user in usernames:
                    target_socket = usernames[target_user]
                    message_data = {
                        "type": "private_message",
                        "timestamp": time.time(),
                        "sender": username,
                        "target": target_user,
                        "content": content,
                    }
                    # Envia a mensagem para o destinatário e para o remetente
                    sockets_to_send = {target_socket, client_socket}
                    broadcast(message_data, sockets_to_send)
                    save_message_to_db(message_data)
                else:
                    # Futuramente: enviar mensagem de erro "usuário não encontrado"
                    pass
            
            # 3.2. Mensagens Públicas (para a sala atual, que por enquanto é só 'geral')
            else:
                message_data = {
                    "type": "public_message",
                    "timestamp": time.time(),
                    "sender": username,
                    "content": msg_content,
                    "room": "geral" # Futuramente, isso será dinâmico
                }
                # Envia para todos na sala 'geral'
                broadcast(message_data, rooms["geral"])
                save_message_to_db(message_data)
            
    except Exception as e:
        print(f"[X] Erro com {username or 'cliente desconhecido'}: {e}")
    
    finally:
        # Remove o cliente da lista
        if client_socket:
            remove_client(client_socket)


# Iniciar o server
def start_server(host='0.0.0.0', port=4242):
    #SOCK_STREAM = TCP e AF_INET = IPv4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Permite reusar a porta logo após fechar

    # Liga o socket ao endereço e porta
    server.bind((host, port))
    server.listen()
    print(f"Servidor de chat rodando em {host}:{port}")
    
    while True:
        # Aceita conexões
        client_socket, addr = server.accept()
        # print(f"[+] Nova conexão de {addr}")
        
        # Criação de thread para o cliente
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
