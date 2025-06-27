import React from 'react';
import './MessageList.css';

function MessageList({ messages }) {
    return (
        <ul className="message-list">
            {messages.length === 0 ? (
                <li className="no-messages">Sem mensagens ainda...</li>
            ) : (
                messages.map((msg, index) => (
                    <li key={index} className="message">
                        {msg}
                    </li>
                ))
            )}
        </ul>
    );
}

export default MessageList;