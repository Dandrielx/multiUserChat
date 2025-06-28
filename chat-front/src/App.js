import React from 'react';
import Chat from './components/Chat/Chat'; // Apenas importa o Chat
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Multi-User Chat</h1>
      </header>
      <div className="App-main-content">
        {/* Renderiza o componente Chat diretamente, sem props */}
        <Chat />
      </div>
    </div>
  );
}

export default App;