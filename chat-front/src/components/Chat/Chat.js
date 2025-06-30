import React, { useState, useEffect, useRef } from 'react';
import websocketService from '../../services/websocketService';
import MessageList from '../MessageList/MessageList';
import MessageInput from '../MessageInput/MessageInput';
import Sidebar from '../Sidebar/Sidebar';
import './Chat.css';

function Chat() {
    const [messages, setMessages] = useState({});
    const [users, setUsers] = useState([]);
    const [activeChat, setActiveChat] = useState('geral');
    const [privateChats, setPrivateChats] = useState([]);
    const [currentUser, setCurrentUser] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [isConnected, setIsConnected] = useState(false);

    // Ele guarda o valor mais recente do currentUser de uma forma que o useEffect pode acessar.
    const currentUserRef = useRef(currentUser);
    useEffect(() => {
        currentUserRef.current = currentUser;
    }, [currentUser]);

    // Este useEffect roda APENAS UMA VEZ na vida do componente.
    useEffect(() => {
        const handleNewMessage = (data) => {
            try {
                const msg = JSON.parse(data);

                if (msg.type === 'user_list') {
                    setUsers(msg.users);
                    return;
                }

                setMessages(prev => {
                    const newMessages = { ...prev };
                    let chatKey;

                    if (msg.type === 'public_message') {
                        chatKey = msg.room;
                    } else if (msg.type === 'private_message') {
                        // Acessa o nome de usuário mais recente através da ref.
                        chatKey = msg.sender === currentUserRef.current ? msg.target : msg.sender;
                        setPrivateChats(p => (p.includes(chatKey) ? p : [...p, chatKey]));
                    }

                    if (chatKey) {
                        if (!newMessages[chatKey]) newMessages[chatKey] = [];
                        newMessages[chatKey] = [...newMessages[chatKey], msg];
                    }

                    return newMessages;
                });
            } catch (error) {
                console.error("Erro ao processar mensagem:", error);
            }
        };

        websocketService.addMessageListener(handleNewMessage);
        websocketService.connect("ws://localhost:3001")
            .then(() => setIsConnected(true))
            .catch(err => console.error("Falha na conexão WS:", err));

        // A função de limpeza roda quando o componente é desmontado.
        return () => {
            websocketService.removeMessageListener(handleNewMessage);
        };
    }, []);

    const handleSendMessage = (message) => {
        if (!isConnected) return;

        if (!isLoggedIn) {
            setCurrentUser(message);
            setIsLoggedIn(true);
            websocketService.sendMessage(message);
        } else {
            if (message.startsWith('/')) {
                websocketService.sendMessage(message);
                if (message.startsWith('/join ')) {
                    const room = message.split(' ')[1];
                    setActiveChat(room);
                } else if (message.startsWith('/priv ')) {
                    const targetUser = message.split(' ')[1];
                    if (!privateChats.includes(targetUser)) {
                        setPrivateChats(p => [...p, targetUser]);
                    }
                    setActiveChat(targetUser);
                }
            } else {
                const currentActiveChat = activeChat;
                if (['geral', 'games', 'estudos'].includes(currentActiveChat)) {
                    websocketService.sendMessage(message);
                } else {
                    websocketService.sendMessage(`/priv ${currentActiveChat} ${message}`);
                }
            }
        }
    };

    const publicRooms = ['geral', 'games', 'estudos'];

    const handleSelectChat = (chatName) => {
        if (publicRooms.includes(chatName) && activeChat !== chatName) {
            websocketService.sendMessage(`/join ${chatName}`);
        }
        setActiveChat(chatName);
    }

    const handleSelectUser = (targetUser) => {
        // Não faz nada se clicar em si mesmo
        if (targetUser === currentUser) return;

        // Adiciona o usuário à lista de chats privados se ele ainda não estiver lá
        if (!privateChats.includes(targetUser)) {
            setPrivateChats(prev => [...prev, targetUser]);
        }

        // Define o chat com esse usuário como o chat ativo
        setActiveChat(targetUser);
    };

    if (!isConnected) return <div>Conectando...</div>;

    return (
        <>
            <Sidebar
                rooms={publicRooms}
                users={users}
                privateChats={privateChats}
                activeChat={activeChat}
                setActiveChat={handleSelectChat}
                currentUser={currentUser}
                onUserSelect={handleSelectUser}
            />
            <div className="chat-view">
                {!isLoggedIn && (
                    <div className="welcome-message">
                        <h2>Bem-vindo ao Chat!</h2>
                        <p>Para começar, digite seu nome de usuário e pressione Enter.</p>
                    </div>
                )}
                <MessageList
                    messages={messages[activeChat] || []}
                    currentUser={currentUser}
                />
                <MessageInput
                    onSend={handleSendMessage}
                    placeholder={!isLoggedIn ? "Digite seu nome..." : `Mensagem em ${activeChat}`}
                />
            </div>
        </>
    );
}

export default Chat;