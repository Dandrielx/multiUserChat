const WebSocket = require('ws');
const net = require('net');

const TCP_HOST = 'localhost';   // muda pra teu host de produção depois
const TCP_PORT = 4242;
const WS_PORT = 3001;          // porta pública pro React

// 1) Sobe WebSocket server
const wss = new WebSocket.Server({ port: WS_PORT }, () =>
    console.log(`🪐 WS proxy na porta ${WS_PORT}`)
);

// 2) Quando browser conecta
wss.on('connection', ws => {
    // Cria conexão TCP com o Python
    const tcp = net.createConnection({ host: TCP_HOST, port: TCP_PORT }, () =>
        console.log('[PROXY] TCP conectado')
    );

    // Browser → Python
    ws.on('message', data => tcp.write(data + '\n'));

    // Python → Browser
    tcp.on('data', chunk => ws.send(chunk.toString()));

    // Limpeza
    const closeAll = () => { try { tcp.end(); } catch { } try { ws.close(); } catch { }; };
    ws.on('close', closeAll);
    tcp.on('end', closeAll);
    tcp.on('error', closeAll);
});
