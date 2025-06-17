# watchdog.py
import socket, subprocess, time

while True:
    try:
        sock = socket.create_connection(('localhost', 4242), timeout=1)
        sock.close()
    except:
        subprocess.Popen(['python', 'backup_server.py'])
        break
    time.sleep(3)
