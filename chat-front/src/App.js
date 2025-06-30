import React from 'react';
import Chat from './components/Chat/Chat';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Multi-User Chat</h1>
      </header>
      <div className="App-main-content">
        <Chat />
      </div>
    </div>
  );
}

export default App;