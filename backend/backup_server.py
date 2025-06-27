import socket, threading
import json
import time

clients = {}
usernames = {}

rooms = {
    "geral": set(),
    "games": set(),
    "estudos": set(),
}

def save_message_to_db(message_data):
    
    pass

def load_message_history(room_or_user_pair):

    return []

def broadcast(message_data, sockets_to_send):
    message_json = json.dumps(message_data)
    for client_socket in list(sockets_to_send):
        try:
            client_socket.send(message_json.encode('utf-8'))
        except:
            remove_client(client_socket)
            
def remove_client(client_socket):
    if client_socket in clients:
        username = clients.pop(client_socket)
        usernames.pop(username, None)
        print(f"[-] {username} desconectado.")

        for room in rooms.values():
            room.discard(client_socket)

        notification = {
            "type": "user_left",
            "timestamp": time.time(),
            "username": username
        }
        broadcast(notification, clients.keys())

def handle_client(client_socket):
    username = None
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()

        if not username or username in usernames:
            print(f"[!] Conexão recusada: username '{username}' é inválido ou já está em uso.")
            client_socket.close()
            return

        clients[client_socket] = username
        usernames[username] = client_socket
        rooms["geral"].add(client_socket)
        
        print(f"[+] {username} se registrou e entrou no chat.")

        join_notification = {"type": "user_joined", "timestamp": time.time(), "username": username}
        broadcast(join_notification, clients.keys())

        user_list_update = {"type": "user_list", "users": list(usernames.keys())}
        client_socket.send(json.dumps(user_list_update).encode('utf-8'))
        
        while True:
            
            msg_content = client_socket.recv(1024).decode('utf-8').strip()
            
            if not msg_content:
                break

            if msg_content.startswith('/priv '):
                parts = msg_content.split(' ', 2)
                if len(parts) < 3:
                    continue
                
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
                    sockets_to_send = {target_socket, client_socket}
                    broadcast(message_data, sockets_to_send)
                    save_message_to_db(message_data)
                else:
                    pass

            else:
                message_data = {
                    "type": "public_message",
                    "timestamp": time.time(),
                    "sender": username,
                    "content": msg_content,
                    "room": "geral" 
                }
                broadcast(message_data, rooms["geral"])
                save_message_to_db(message_data)
            
    except Exception as e:
        print(f"[X] Erro com {username or 'cliente desconhecido'}: {e}")
    
    finally:
        if client_socket:
            remove_client(client_socket)

def start_server(host='0.0.0.0', port=4243):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((host, port))
    server.listen()
    print(f"Servidor BACKUP rodando em {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
