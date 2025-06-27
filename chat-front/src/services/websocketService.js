class WebSocketService {
    constructor() {
        this.socket = null;
        this.messageListeners = [];
    }

    connect(url) {
        // Se já estiver conectado, não faz nada
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            return Promise.resolve();
        }

        // Se estiver conectando, espera a conexão atual terminar
        if (this.connectingPromise) {
            return this.connectingPromise;
        }

        this.connectingPromise = new Promise((resolve, reject) => {
            this.socket = new WebSocket(url);

            this.socket.onopen = () => {
                console.log("WS Conectado");
                this.connectingPromise = null; // Limpa a promise de conexão
                resolve();
            };

            this.socket.onmessage = (event) => {
                // Quando uma mensagem chega, notifica todos os ouvintes
                this.messageListeners.forEach(listener => listener(event.data));
            };

            this.socket.onclose = () => {
                console.log("WS Desconectado");
                this.socket = null;
                this.connectingPromise = null;
            };

            this.socket.onerror = (error) => {
                console.error("WS Erro:", error);
                this.connectingPromise = null;
                reject(error);
            };

            window.ws = this.socket; // Para debug
        });

        return this.connectingPromise;
    }

    // Adiciona um ouvinte de mensagens
    addMessageListener(callback) {
        this.messageListeners.push(callback);
    }

    // Remove um ouvinte de mensagens
    removeMessageListener(callback) {
        this.messageListeners = this.messageListeners.filter(
            (listener) => listener !== callback
        );
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