class WebSocketService {
    constructor() {
        this.socket = null;
    }

    connect(url, onMessageCallback) {
        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(url);

            this.socket.onopen = () => {
                console.log("WS Conectado");
                resolve();
            };

            this.socket.onmessage = (event) => {
                console.log("[FRONT] Mensagem recebida:", event.data);
                if (onMessageCallback) {
                    onMessageCallback(event.data);
                }
            };

            this.socket.onclose = () => {
                console.log("WS Desconectado");
            };

            this.socket.onerror = (error) => {
                console.error("WS Erro:", error);
                reject(error);
            };

            // Para debug no console
            window.ws = this.socket;
        });
    }

    sendMessage(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(message);
        } else {
            console.error("WebSocket não está conectado.");
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

const websocketService = new WebSocketService();
export default websocketService;