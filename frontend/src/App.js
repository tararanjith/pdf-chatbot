import React, { useState } from "react";
import PDFUpload from "./components/PDFUpload";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import axios from "axios";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);

  const handleSend = async (userMsg) => {
    const newUserMessage = { sender: "user", text: userMsg };
    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);

    const formattedHistory = updatedMessages.map((msg) => ({
      role: msg.sender === "user" ? "user" : "assistant",
      content: msg.text,
    }));

    try {
      const res = await axios.post(
        "http://localhost:5000/chat",
        {
          query: userMsg,
          history: formattedHistory,
        },
        {
          withCredentials: true, // ✅ Needed for Flask session to persist
        }
      );

      const botReply = { sender: "bot", text: res.data.response };
      setMessages((prev) => [...prev, botReply]);
    } catch (err) {
      console.error("Chat error:", err); // Optional: log actual error
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Something went wrong." },
      ]);
    }
  };

  return (
    <div className="app">
      <h1>AI PDF Chatbot</h1>
      <PDFUpload onUploadSuccess={() => alert("Ready to chat!")} />
      <ChatWindow messages={messages} />
      <ChatInput onSend={handleSend} />
    </div>
  );
}

export default App;
