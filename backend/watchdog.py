import socket
import subprocess
import time
import psutil  # pip install psutil

MAIN_HOST = 'localhost'
MAIN_PORT = 4242
BACKUP_PROCESS = None

def is_alive(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except:
        return False

def kill_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and isinstance(cmdline, list):
            if name in ' '.join(cmdline):
                print(f"[WATCHDOG] Matando processo: {proc.info['pid']} ({name})")
                proc.kill()

while True:
    principal_online = is_alive(MAIN_HOST, MAIN_PORT)

    if principal_online:
        print("[WATCHDOG] Principal OK.")
        if BACKUP_PROCESS:
            print("[WATCHDOG] Principal voltou! Matando o backup.")
            kill_process_by_name("backup_server.py")
            BACKUP_PROCESS = None
    else:
        print("[WATCHDOG] Principal OFFLINE.")
        if BACKUP_PROCESS is None:
            print("[WATCHDOG] Subindo backup...")
            BACKUP_PROCESS = subprocess.Popen(["python", "backup_server.py"])
    time.sleep(3)
