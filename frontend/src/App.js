import React, { useState } from "react";
import PDFUpload from "./components/PDFUpload";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (userMsg) => {
    setMessages(prev => [...prev, { sender: "user", text: userMsg }]);

    try {
      const res = await axios.post("http://localhost:5000/chat", { query: userMsg });
      setMessages(prev => [...prev, { sender: "bot", text: res.data.response }]);
    } catch (err) {
      setMessages(prev => [...prev, { sender: "bot", text: "Something went wrong." }]);
    }
  };

  return (
    <div className="app">
      <h1>📚 AI PDF Chatbot</h1>
      <PDFUpload onUploadSuccess={() => alert("Ready to chat!")} />
      <ChatWindow messages={messages} />
      <ChatInput onSend={handleSend} />
    </div>
  );
}

export default App;
