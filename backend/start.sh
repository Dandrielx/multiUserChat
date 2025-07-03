# start.sh
#!/usr/bin/env bash

# inicializa o watch dog 
python watchdog.py &
# inicializa o server em primeiro plano
python server.py