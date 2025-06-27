import React, { useState, useEffect } from 'react';
import websocketService from '../../services/websocketService';
import MessageList from '../MessageList/MessageList';
import MessageInput from '../MessageInput/MessageInput';
import './Chat.css';

function Chat() {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        const handleNewMessage = (newMessage) => {
            setMessages((prevMessages) => [...prevMessages, newMessage]);
        };

        websocketService.connect("ws://localhost:3001", handleNewMessage)
            .catch(err => console.error("Falha na conexão com o WebSocket:", err));

        return () => {
            websocketService.disconnect();
        };
    }, []);

    const handleSend = (message) => {
        websocketService.sendMessage(message);
    };

    return (
        <div className="chat-container">
            <MessageList messages={messages} />
            <MessageInput onSend={handleSend} />
        </div>
    );
}

export default Chat;