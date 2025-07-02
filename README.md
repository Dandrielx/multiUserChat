# Multi-User Chat

Este é um projeto de chat multi-usuário composto por um frontend em React, um backend em Python e um proxy em Node.js para conectar os dois.

## Arquitetura

O projeto é dividido em três partes principais:

1.  `chat-front/`: A aplicação frontend construída com React.
2.  `backend/`: O servidor principal do chat, escrito em Python, que gerencia as salas e as mensagens.
3.  `proxy/`: Um servidor proxy Node.js que atua como uma ponte, convertendo as conexões WebSocket (WS) do frontend para conexões TCP que o backend Python pode entender.

## Como Rodar Localmente

Para executar o projeto completo, você precisará ter o **Node.js** (com npm) e o **Python 3** instalados em sua máquina.

Siga os passos abaixo, executando cada comando em um terminal separado.

### 1. Backend (Servidor Python)

O backend é responsável pela lógica principal do chat. Ele utiliza apenas bibliotecas padrão do Python, portanto, não é necessário instalar dependências com `pip`.

```bash
# Navegue até a pasta do backend
cd backend

# Inicie o servidor principal
python server.py
```

O servidor começará a rodar e a aguardar conexões na porta `4242`.

### 2. Proxy (Node.js)

O proxy é essencial para que o frontend (que usa WebSockets) possa se comunicar com o backend (que usa TCP sockets).

```bash
# Em um NOVO terminal, navegue até a pasta do proxy
cd proxy

# Instale as dependências
npm install

# Inicie o proxy
node index.js
```

O proxy irá rodar na porta `3001` e se conectará ao servidor Python na porta `4242`.

### 3. Frontend (React)

O frontend é a interface com a qual o usuário interage.

```bash
# Em um TERCEIRO terminal, navegue até a pasta do frontend
cd chat-front

# Instale as dependências
npm install

# Inicie a aplicação React
npm start
```

Após a compilação, seu navegador deve abrir automaticamente no endereço `http://localhost:3000`. Se não abrir, acesse-o manualmente.

---

### Conclusão

Ao final desses passos, você terá o ambiente completo rodando:

-   O **servidor Python** escutando na porta `4242`.
-   O **proxy Node.js** escutando na porta `3001`.
-   A **aplicação React** rodando na porta `3000`.

Agora você pode testar o chat localmente!
