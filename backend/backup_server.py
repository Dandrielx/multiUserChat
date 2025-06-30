import socket
import threading
import json
import time

# ARQUIVO IGUAL AO server.py

clients = {}
usernames = {}
client_rooms = {}
rooms = {"geral": set(), "games": set(), "estudos": set()}

def broadcast_user_list():
    user_list_update = {
        "type": "user_list",
        "users": list(usernames.keys())
    }
    broadcast(user_list_update, clients.keys())

def broadcast(message_data, sockets_to_send):
    message_json = json.dumps(message_data)
    for client_socket in list(sockets_to_send):
        try:
            client_socket.send(message_json.encode('utf-8'))
        except:
            remove_client(client_socket)

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

def handle_client(client_socket):
    username = None
    try:
        username = client_socket.recv(1024).decode('utf-8').strip()
        if not username or username in usernames:
            client_socket.close()
            return

        clients[client_socket] = username
        usernames[username] = client_socket
        client_rooms[client_socket] = "geral"
        rooms["geral"].add(client_socket)
        
        print(f"[+] {username} conectado à sala 'geral'.")
        broadcast_user_list()

        while True:
            msg_content = client_socket.recv(1024).decode('utf-8').strip()
            if not msg_content: break

            if msg_content.startswith('/'):
                parts = msg_content.split(' ', 2)
                command = parts[0]

                if command == '/join' and len(parts) == 2:
                    new_room = parts[1]
                    if new_room in rooms:
                        old_room = client_rooms[client_socket]
                        rooms[old_room].discard(client_socket)
                        rooms[new_room].add(client_socket)
                        client_rooms[client_socket] = new_room
                        print(f"[*] {username} trocou para a sala '{new_room}'")
                    continue

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

def start_server(host='0.0.0.0', port=4242):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    print(f"Servidor de chat BACKUP rodando em {host}:{port}")
    
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
