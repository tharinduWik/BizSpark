import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [items, setItems] = useState([]);
  const [sessionId, setSessionId] = useState('');
  const [activeView, setActiveView] = useState('chat'); // 'chat', 'items', 'about'
  const [suggestions, setSuggestions] = useState([]);
  
  // Initialize session and fetch initial data
  useEffect(() => {
    // Generate a session ID if none exists yet
    const newSessionId = sessionStorage.getItem('chatSessionId') || uuidv4();
    sessionStorage.setItem('chatSessionId', newSessionId);
    setSessionId(newSessionId);
    
    // Add welcome message when chat starts
    if (messages.length === 0) {
      sendWelcomeMessage(newSessionId);
    }
    
    // Load all items
    fetchAllItems();
  }, []);
  
  const fetchAllItems = async () => {
    try {
      const response = await fetch('http://localhost:8000/items');
      const data = await response.json();
      setItems(data.items || []);
    } catch (err) {
      console.error('Error fetching items:', err);
    }
  };

  const sendWelcomeMessage = async (sid = sessionId) => {
    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: 'hello',
          session_id: sid
        })
      });
      const data = await response.json();
      addMessage('bot', data);
      // Set suggestions from welcome response
      if (data.suggestions) {
        setSuggestions(data.suggestions);
      }
    } catch (err) {
      console.error('Error fetching welcome message:', err);
      addMessage('bot', {
        response: "👋 Welcome to our Business Assistant! I'm here to help you find the perfect products for your needs. How can I assist you today?",
        suggestions: [
          "Show me laptops under $500",
          "Do you have any office supplies?",
          "What are your best-selling items?"
        ]
      });
      setSuggestions([
        "Show me laptops under $500",
        "Do you have any office supplies?",
        "What are your best-selling items?"
      ]);
    }
  };

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;
    
    // Clear suggestions when user sends a message
    setSuggestions([]);
    
    // Add user message to chat
    addMessage('user', { query: message.trim() });
    
    // Set loading state
    setLoading(true);
    setError(null);

    try {
      // Include session ID with each query
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: message.trim(),
          session_id: sessionId
        })
      });
      const data = await response.json();
      
      // Add AI response to chat
      addMessage('bot', data);
      
      // Set new suggestions if provided
      if (data.suggestions) {
        setSuggestions(data.suggestions);
      }
    } catch (err) {
      setError('Failed to get response. Please try again.');
      addMessage('system', { 
        message: 'Failed to get response from assistant. Please try again.',
        type: 'error'
      });
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleSendMessage(suggestion);
  };

  const addMessage = (type, data) => {
    const newMessage = {
      type,
      data,
      timestamp: new Date()
    };
    
    setMessages(prevMessages => [...prevMessages, newMessage]);
  };

  const renderChat = () => {
    return (
      <ChatWindow
        messages={messages}
        onSendMessage={handleSendMessage}
        loading={loading}
        suggestions={suggestions}
        onSuggestionClick={handleSuggestionClick}
      />
    );
  };

  const renderItems = () => {
    return (
      <div className="items-view">
        <h2>Available Items</h2>
        {items.length === 0 ? (
          <p className="loading">Loading items...</p>
        ) : (
          <div className="items-grid">
            {items.map((item, index) => (
              <div key={index} className="item-card">
                <div className="item-name">{item.name || item.item_name}</div>
                <div className="item-price">
                  ${(item.price || item.item_price || 0).toFixed(2)}
                </div>
                {item.description && (
                  <div className="item-description">{item.description}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderAbout = () => {
    return (
      <div className="about-view">
        <h2>About BizSpark</h2>
        <p>
          I'm your AI-powered business assistant, designed to help you find and learn about our products.
          I can assist you with:
        </p>
        <ul>
          <li>Finding products based on your requirements</li>
          <li>Answering questions about specific items</li>
          <li>Providing recommendations within your budget</li>
          <li>Explaining product features and specifications</li>
        </ul>
        <p>
          Simply start a conversation in the chat tab, and I'll be happy to help you find exactly what you need!
        </p>
      </div>
    );
  };

  const renderCurrentView = () => {
    switch (activeView) {
      case 'items':
        return renderItems();
      case 'about':
        return renderAbout();
      default:
        return renderChat();
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <div className="header-container">
          <div className="logo">
            <h1 className="logo-text">BizSpark</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div style={{ width: '100%', maxWidth: '800px' }}>
          {/* Navigation Tabs */}
          <div className="nav-tabs">
            <button 
              className={`nav-tab ${activeView === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveView('chat')}
            >
              Chat
            </button>
            <button 
              className={`nav-tab ${activeView === 'items' ? 'active' : ''}`}
              onClick={() => setActiveView('items')}
            >
              Items ({items.length})
            </button>
            <button 
              className={`nav-tab ${activeView === 'about' ? 'active' : ''}`}
              onClick={() => setActiveView('about')}
            >
              About
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="error">
              {error}
              <button 
                style={{ marginLeft: '10px', background: 'none', border: 'none', color: 'inherit', cursor: 'pointer' }}
                onClick={() => setError(null)}
              >
                ×
              </button>
            </div>
          )}

          {/* Current View */}
          {renderCurrentView()}
        </div>
      </main>
    </div>
  );
}

export default App;
