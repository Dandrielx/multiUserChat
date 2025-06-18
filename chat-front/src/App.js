import { useEffect, useState } from "react";

function App() {
  const [ws, setWs] = useState(null);
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    const sock = new WebSocket("ws://localhost:3001");
    sock.onopen = () => console.log("WS conectado");
    sock.onmessage = (e) => {
      console.log("[FRONT] Mensagem recebida:", e.data);
      setMsgs((prev) => [...prev, e.data]);
    };
    setWs(sock);
    // Torna o socket acessível no console
    window.ws = sock;
    return () => sock.close();
  }, []);

  const send = () => {
    if (ws && input.trim()) {
      ws.send(input);
      setInput("");
    }
  };

  return (
    <div>
      <ul>
        {msgs.length === 0 ? <li>Sem mensagens ainda...</li> : null}
        {msgs.map((m, i) => (
          <li key={i} style={{ marginBottom: "5px" }}>{m}</li>
        ))}
      </ul>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={send}>Enviar</button>
    </div>
  );
}

export default App;
