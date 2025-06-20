import socket, subprocess, time, psutil

MAIN_HOST = 'localhost'
MAIN_PORT = 4242
BACKUP_PROCESS = None
pre_state = None  # pode ser 'ok' ou 'down'

def is_alive(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except:
        return False

def kill_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and isinstance(cmdline, list):
            if name in ' '.join(cmdline):
                print(f"[WATCHDOG] Matando processo: {proc.info['pid']} ({name})")
                proc.kill()

while True:
    principal_online = is_alive(MAIN_HOST, MAIN_PORT)

    if principal_online:
        if pre_state != 'ok':
            print("[WATCHDOG] Principal voltou!")
            pre_state = 'ok'
        if BACKUP_PROCESS:
            kill_process_by_name("backup_server.py")
            BACKUP_PROCESS = None
    else:
        if pre_state != 'down':
            print("[WATCHDOG] Principal OFFLINE. Subindo backup...")
            pre_state = 'down'
        if BACKUP_PROCESS is None:
            BACKUP_PROCESS = subprocess.Popen(["python", "backup_server.py"])

    time.sleep(3)
