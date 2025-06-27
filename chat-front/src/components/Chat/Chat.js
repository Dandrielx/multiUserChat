import React, { useState, useEffect } from 'react';
import websocketService from '../../services/websocketService';
import MessageList from '../MessageList/MessageList';
import MessageInput from '../MessageInput/MessageInput';
import './Chat.css';

// O componente agora recebe o 'username' de quem está logado
function Chat({ username }) {
    const [messages, setMessages] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [currentUser, setCurrentUser] = useState('');

    useEffect(() => {
        // Funçao que recebe a string JSON
        const handleNewMessage = (data) => {
            try {
                // Transformamos a string de volta em um objeto JavaScript
                const messageObject = JSON.parse(data);
                setMessages((prevMessages) => [...prevMessages, messageObject]);
            } catch (error) {
                // Se a mensagem não for um JSON válido, apenas a exibimos como texto
                console.error("Erro ao parsear a mensagem JSON:", error);
                // setMessages((prevMessages) => [...prevMessages, { type: 'raw', content: data }]);
            }
        };

        // Adiciona o ouvinte de mensagens
        websocketService.addMessageListener(handleNewMessage);

        // Conectamos e, logo em seguida, enviamos o nome do usuário para o servidor
        websocketService.connect("ws://localhost:3001", handleNewMessage)
            .then(() => {
                // O backend agora espera o nome do usuário como primeira mensagem
                setIsConnected(true);
                console.log("Conectado ao servidor. Aguardando nome de usuário...");
            })
            .catch(err => {
                console.error("Falha na conexão com o WebSocket:", err);
                setIsConnected(false);
            });
        return () => {
            websocketService.removeMessageListener(handleNewMessage);
        };
        // Adicionamos 'username' como dependência para reconectar se o usuário mudar
    }, [username]);

    const handleSend = (message) => {
        if (!isConnected) return;

        // Se ainda não estiver logado, esta mensagem é o nome de usuário.
        if (!isLoggedIn) {
            setCurrentUser(message); // Define o nome de usuário no estado
            websocketService.sendMessage(message);
            setIsLoggedIn(true); // Marca que o login foi feito
            console.log(`Usuário "${message}" enviado para o servidor.`);
        } else {
            // Se já estiver logado, envia como uma mensagem de chat normal.
            websocketService.sendMessage(message);
        }
    };
    if (!isConnected) {
        return <div>Conectando ao servidor de chat...</div>;
    }

    return (
        <div className="chat-container">
            {/* Mostra uma mensagem de boas-vindas se ainda não estiver logado */}
            {!isLoggedIn && (
                <div className="welcome-message">
                    <h2>Bem-vindo!</h2>
                    <p>Digite seu nome no campo abaixo e pressione Enter para entrar.</p>
                </div>
            )}
            <MessageList messages={messages} currentUser={currentUser} />
            <MessageInput
                onSend={handleSend}
                // Muda o placeholder do input para guiar o usuário
                placeholder={!isLoggedIn ? "Digite seu nome..." : "Digite sua mensagem..."}
            />
        </div>
    );
}

export default Chat;