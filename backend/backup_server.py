import socket
import threading
import json
import time
import os

# Estruturas principais
clients = {}  # socket -> username
usernames = {}  # username -> socket
client_rooms = {}  # socket -> sala atual
rooms = {"geral": set(), "games": set(), "estudos": set()}  # salas disponíveis

print(f"[BACKUP SERVER] Starting...")

# Envia a lista atualizada de usuários pra todos os clientes
def broadcast_user_list():
    user_list_update = {
        "type": "user_list",
        "users": list(usernames.keys())
    }
    broadcast(user_list_update, clients.keys())

# Envia uma mensagem (em JSON) pra um conjunto de sockets
def broadcast(message_data, sockets_to_send):
    message_json = json.dumps(message_data)
    for client_socket in list(sockets_to_send):
        try:
            client_socket.send(message_json.encode('utf-8'))
        except:
            remove_client(client_socket)  # Remove se der ruim no envio

# Remove cliente das estruturas internas e das salas
def remove_client(client_socket):
    if client_socket in clients:
        username = clients.pop(client_socket, None)
        if username:
            usernames.pop(username, None)
            print(f"[-] {username} desconectado.")
            broadcast_user_list()
        
        current_room = client_rooms.pop(client_socket, None)
        if current_room in rooms:
            rooms[current_room].discard(client_socket)

# Lida com a conexão de um cliente
def handle_client(client_socket):
    username = None
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()
        if not username or username in usernames:
            client_socket.close()
            return
        
        # Registra cliente
        clients[client_socket] = username
        usernames[username] = client_socket
        client_rooms[client_socket] = "geral"
        rooms["geral"].add(client_socket)
        
        print(f"[+] {username} conectado à sala 'geral'.")
        broadcast_user_list()

        # Loop principal da thread do cliente
        while True:
            msg_content = client_socket.recv(1024).decode('utf-8').strip()
            if not msg_content: break

            # Comandos iniciados com '/'
            if msg_content.startswith('/'):
                parts = msg_content.split(' ', 2)
                command = parts[0]

                # Troca de sala
                if command == '/join' and len(parts) == 2:
                    new_room = parts[1]
                    if new_room in rooms:
                        old_room = client_rooms[client_socket]
                        rooms[old_room].discard(client_socket)
                        rooms[new_room].add(client_socket)
                        client_rooms[client_socket] = new_room
                        print(f"[*] {username} trocou para a sala '{new_room}'")
                    continue
                
                # Mensagem privada
                elif command == '/priv' and len(parts) >= 3:
                    target_user, content = parts[1], parts[2]
                    if target_user in usernames:
                        target_socket = usernames[target_user]
                        message_data = {
                            "type": "private_message",
                            "timestamp": time.time(),
                            "sender": username,
                            "target": target_user,
                            "content": content
                        }
                        broadcast(message_data, {target_socket, client_socket})
                    continue

            # Mensagem pública pra sala atual
            else:
                current_room = client_rooms.get(client_socket, "geral")
                message_data = {
                    "type": "public_message",
                    "timestamp": time.time(),
                    "sender": username,
                    "room": current_room,
                    "content": msg_content
                }
                if current_room in rooms:
                    broadcast(message_data, rooms[current_room])

    except Exception:
        pass
    finally:
        if client_socket:
            remove_client(client_socket)

# Inicia o servidor principal
def start_server(host='0.0.0.0', port=4242):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    print(f"Servidor backup de chat rodando em {host}:{port}")
    
    while True:
        print("[BACKEND] Waiting for new connection…")
        try:
            client_socket, addr = server.accept()
            print(f"[BACKEND] → Connection accepted from {addr}")
        except Exception as e:
            print(f"[BACKEND] ! accept() error:", e)
            continue

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4242))
    start_server(port = port)