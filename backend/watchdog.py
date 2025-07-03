import socket, subprocess, time, psutil, os

MAIN_HOST = "localhost"     # Endereço do servidor principal
MAIN_PORT = int(os.environ.get("PORT", 4242))            # Porta do servidor principal
BACKUP_PROCESS = None       # Referência pro processo do servidor backup
pre_state = None            # Estado anterior (pra evitar prints repetidos)

time.sleep(10)

# Verifica se o servidor principal está respondendo
def is_alive(host, port):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except:
        return False

# Mata processos com o nome especificado
def kill_process_by_name(name):
    for proc in psutil.process_iter(['pid', 'cmdline']):
        cmdline = proc.info.get('cmdline')
        if cmdline and isinstance(cmdline, list):
            if name in ' '.join(cmdline):  # Checa se o nome tá na linha de comando
                print(f"[WATCHDOG] Matando processo: {proc.info['pid']} ({name})")
                proc.kill()

# Loop principal do watchdog
while True:
    principal_online = is_alive(MAIN_HOST, MAIN_PORT)

    if principal_online:
        # Caso o principal volte, mata o backup se estiver rodando
        if pre_state != 'ok':
            print("[WATCHDOG] Principal voltou!")
            pre_state = 'ok'
        if BACKUP_PROCESS:
            kill_process_by_name("backup_server.py")
            BACKUP_PROCESS = None
    else:
        # Caso o principal caia, sobe o backup
        if pre_state != 'down':
            print("[WATCHDOG] Principal OFFLINE. Subindo backup...")
            pre_state = 'down'
        if BACKUP_PROCESS is None:
            BACKUP_PROCESS = subprocess.Popen(["python", "backup_server.py"])

    time.sleep(3)  # Espera 3 segundos antes de checar de novo
