import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import './ChatWindow.css';

const ChatWindow = ({ 
  messages, 
  onSendMessage, 
  loading, 
  suggestions, 
  onSuggestionClick 
}) => {
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'end'
    });
  };

  const renderTypingIndicator = () => {
    if (!loading) return null;
    
    return (
      <div className="typing-indicator">
        <div className="typing-bubble">
          <div className="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    );
  };

  const renderWelcomeMessage = () => {
    if (messages.length > 0) return null;
    
    return (
      <div className="welcome-message">
        <div className="welcome-icon">💼</div>
        <h3>Welcome to BizSpark</h3>
        <p>I'm here to help you find the perfect products for your business needs. 
           Feel free to ask me about our inventory, get recommendations, or inquire about pricing!</p>
      </div>
    );
  };

  return (
    <div className="chat-window">
      {/* Chat Header */}
      <div className="chat-header">
        <div className="chat-header-info">
          <div className="assistant-avatar">🤖</div>
          <div className="assistant-details">
            <div className="assistant-name">BizSpark</div>
            <div className="assistant-status">
              <span className="status-dot"></span>
              Online
            </div>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="chat-messages" ref={chatContainerRef}>
        <div className="messages-container">
          {renderWelcomeMessage()}
          
          {messages.map((message, index) => (
            <MessageBubble
              key={index}
              message={message}
              isUser={message.type === 'user'}
              timestamp={message.timestamp}
            />
          ))}
          
          {renderTypingIndicator()}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <InputBox
        onSendMessage={onSendMessage}
        loading={loading}
        suggestions={suggestions}
        onSuggestionClick={onSuggestionClick}
      />
    </div>
  );
};

export default ChatWindow;
