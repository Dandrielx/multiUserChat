const WebSocket = require('ws');
const net = require('net');

const TCP_HOST = process.env.TCP_HOST;   // muda pra teu host de produção depois
const TCP_PORT = parseInt(process.env.TCP_PORT, 10) || 4242;
const WS_PORT = parseInt(process.env.PORT, 10) || 3001;;          // porta pública pro React
console.log('Funfou');

// Sobe WebSocket server
const wss = new WebSocket.Server({ port: WS_PORT }, () =>
    console.log(`WS proxy na porta ${WS_PORT}`)
);

// Quando browser conecta
wss.on('connection', ws => {
    // Cria conexão TCP com o Python
    console.log('[PROXY] 🔌 New WS client connected');
    const tcp = net.createConnection({ host: TCP_HOST, port: TCP_PORT, family: 4 }, () =>
        console.log('[PROXY] TCP conectado')
    );

    tcp.on('error', err => {
        console.error('[PROXY] TCP connection error:', err.message);
    });

    // Front -> Back
    ws.on('message', data => tcp.write(data + '\n'));

    // Back -> Front
    tcp.on('data', chunk => ws.send(chunk.toString()));

    // Limpeza
    const closeAll = () => { try { tcp.end(); } catch { } try { ws.close(); } catch { }; };
    ws.on('close', closeAll);
    tcp.on('end', closeAll);
    tcp.on('error', closeAll);
});
