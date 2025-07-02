# 🗨️ Multi-User Chat

Este é um projeto de chat multi-usuário composto por um frontend em React, um backend em Python e um proxy em Node.js para conectar os dois. Todo o projeto está organizado dentro da pasta `backend/`, com as subpastas `proxy/` e `chat-front/`.

---

## 🛠️ Como Rodar Localmente

Para executar o projeto completo, você precisará ter o **Node.js** (com `npm`) e o **Python 3** instalados em sua máquina. Execute cada comando abaixo em um terminal separado.

---

### 🔄 Primeiro terminal: Backend (Python)

cd backend
python server.py
O servidor começará a rodar e a aguardar conexões na porta 4242.

🔄 Segundo terminal: Proxy (Node.js)

cd backend/proxy
npm install
node index.js
O proxy irá rodar na porta 3001 e se conectará ao servidor Python na porta 4242.

🔄 Terceiro terminal: Frontend (React)

cd backend/chat-front
npm install
npm start
Após a compilação, seu navegador deve abrir automaticamente no endereço http://localhost:3000. Se não abrir, acesse manualmente.
