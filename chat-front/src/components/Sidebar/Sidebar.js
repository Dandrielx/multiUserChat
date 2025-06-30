import React from 'react';
import './Sidebar.css';

function Sidebar({ rooms, users, privateChats, activeChat, setActiveChat, currentUser, onUserSelect }) {
    return (
        <div className="sidebar">
            <div className="sidebar-section">
                <h3>Salas Públicas</h3>
                <ul>
                    {rooms.map(room => (
                        <li
                            key={room}
                            className={activeChat === room ? 'active' : ''}
                            onClick={() => setActiveChat(room)}
                        >
                            # {room}
                        </li>
                    ))}
                </ul>
            </div>

            <div className="sidebar-section">
                <h3>Chats Privados</h3>
                <ul>
                    {privateChats.map(chatName => (
                        <li
                            key={chatName}
                            className={activeChat === chatName ? 'active' : ''}
                            onClick={() => setActiveChat(chatName)}
                        >
                            <span className="status-indicator private"></span>
                            {chatName}
                        </li>
                    ))}
                </ul>
            </div>

            <div className="sidebar-section">
                <h3>Usuários Online</h3>
                <ul>
                    {users.map(user => {
                        const isYou = user === currentUser;
                        const isClickable = !isYou;

                        return (
                            <li
                                key={user}
                                className={`user-item ${isClickable ? 'clickable' : ''}`}
                                onClick={isClickable ? () => onUserSelect(user) : undefined}
                            >
                                <span className="status-indicator online"></span>
                                {user} {isYou && '(Você)'}
                            </li>
                        );
                    })}
                </ul>
            </div>
        </div>
    );
}

export default Sidebar;