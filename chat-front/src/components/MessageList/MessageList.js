import React, { useEffect, useRef } from 'react';
import './MessageList.css';

// Recebe o currentUser para saber quem é
function MessageList({ messages, currentUser }) {
    const messagesEndRef = useRef(null);

    // Função para rolar para a mensagem mais recente
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    return (
        <ul className="message-list">
            {messages.map((msg, index) => {
                // Tratamento para notificações
                if (msg.type === 'user_joined' || msg.type === 'notification') {
                    return <li key={index} className="notification">{msg.content || `${msg.username} entrou`}</li>;
                }
                if (msg.type === 'user_left') {
                    return <li key={index} className="notification">{`${msg.username} saiu`}</li>;
                }

                // Tratamento para mensagens normais
                if (msg.type === 'public_message' || msg.type === 'private_message') {
                    const isSentByCurrentUser = msg.sender === currentUser;
                    const messageClass = isSentByCurrentUser ? 'message-sent' : 'message-received';

                    return (
                        <li key={index} className={`message-container ${isSentByCurrentUser ? 'sent' : 'received'}`}>
                            <div className={`message-bubble ${messageClass}`}>
                                {!isSentByCurrentUser && <div className="sender-name">{msg.sender}</div>}
                                <div className="message-content">{msg.content}</div>
                            </div>
                        </li>
                    );
                }

                // Retorno padrão para qualquer outro tipo de dado inesperado
                return null;
            })}
            <div ref={messagesEndRef} />
        </ul>
    );
}

export default MessageList;