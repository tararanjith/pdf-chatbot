// src/components/ChatSection.js
import React, { useState } from 'react';
import axios from 'axios';

const ChatSection = () => {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!query.trim()) return;

    const newMessages = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    setQuery('');

    try {
      const res = await axios.post(
        'http://localhost:5000/chat',
        { query, history: newMessages },
        {
          withCredentials: true,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      const reply = res.data.response;
      setMessages([...newMessages, { role: 'assistant', content: reply }]);
    } catch (err) {
      console.error('Chat error', err);
      alert('Something went wrong.');
    }
  };

  return (
    <div className="w-full max-w-2xl bg-zinc-900 rounded-xl shadow-lg p-6 flex flex-col gap-4">
      <div className="h-96 overflow-y-auto border border-zinc-700 rounded-lg p-4 space-y-3 bg-black">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 rounded-md ${
              msg.role === 'user' ? 'bg-red-800 text-right' : 'bg-zinc-800 text-left'
            }`}
          >
            <p>{msg.content}</p>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          className="flex-1 px-4 py-2 rounded-lg bg-zinc-800 text-white border border-zinc-600"
          placeholder="Ask something..."
        />
        <button
          onClick={handleSend}
          className="bg-red-600 hover:bg-red-700 transition-all px-4 py-2 rounded text-white font-semibold"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatSection;
