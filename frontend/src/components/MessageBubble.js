import React from "react";
import ReactMarkdown from "react-markdown";

const MessageBubble = ({ sender, text }) => {
  return (
    <div className={`message-bubble ${sender}`}>
      <ReactMarkdown>{text}</ReactMarkdown>
    </div>
  );
};

export default MessageBubble;
