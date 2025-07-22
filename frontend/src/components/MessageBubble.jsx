import React from 'react';
import './MessageBubble.css';

const MessageBubble = ({ message, isUser, timestamp }) => {
  const formatTime = (date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).format(new Date(date));
  };

  const renderMessageContent = () => {
    if (isUser) {
      return <p className="message-text">{message.data.query}</p>;
    } else {
      // Bot message
      return (
        <div className="bot-message-content">
          <p className="message-text">{message.data.response}</p>
          
          {/* Display single item if it exists */}
          {message.data.item_data && (
            <div className="recommended-items">
              <h4>🔍 Product Details:</h4>
              <div className="items-list">
                <div className="item-card detailed-item">
                  <div className="item-name">{message.data.item_data.item_name}</div>
                  <div className="item-price">
                    ${message.data.item_data.price.toFixed(2)}
                    {message.data.item_data.maximum_discount > 0 && (
                      <span className="discount-badge">
                        {(message.data.item_data.maximum_discount * 100).toFixed(0)}% discount available
                      </span>
                    )}
                  </div>
                  {message.data.item_data.item_description && (
                    <div className="item-description">{message.data.item_data.item_description}</div>
                  )}
                  <div className="item-stock">
                    Stock: <span className={message.data.item_data.item_quantity > 10 ? "in-stock" : "low-stock"}>
                      {message.data.item_data.item_quantity} available
                    </span>
                  </div>
                  <div className="item-id">SKU: {message.data.item_data.item_id}</div>
                </div>
              </div>
            </div>
          )}
          
          {/* Display multiple items if they exist */}
          {!message.data.item_data && message.data.items && message.data.items.length > 0 && (
            <div className="recommended-items">
              <h4>💡 Product Selection:</h4>
              <div className="items-list">
                {message.data.items.map((item, index) => (
                  <div key={index} className="item-card">
                    <div className="item-name">{item.item_name}</div>
                    <div className="item-price">
                      ${item.price.toFixed(2)}
                      {item.maximum_discount > 0 && (
                        <span className="discount-badge">
                          {(item.maximum_discount * 100).toFixed(0)}% discount
                        </span>
                      )}
                    </div>
                    {item.item_description && (
                      <div className="item-description">{item.item_description}</div>
                    )}
                    <div className="item-stock">
                      <span className={item.item_quantity > 10 ? "in-stock" : "low-stock"}>
                        {item.item_quantity} in stock
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* For backward compatibility */}
          {!message.data.item_data && !message.data.items && message.data.recommended_items && message.data.recommended_items.length > 0 && (
            <div className="recommended-items">
              <h4>💡 Recommended Items:</h4>
              <div className="items-list">
                {message.data.recommended_items.map((item, index) => (
                  <div key={index} className="item-card">
                    <div className="item-name">{item.name || item.item_name}</div>
                    <div className="item-price">
                      ${(item.price || item.item_price || 0).toFixed(2)}
                      {item.maximum_discount > 0 && (
                        <span className="discount-badge">
                          {(item.maximum_discount * 100).toFixed(0)}% discount
                        </span>
                      )}
                    </div>
                    {(item.description || item.item_description) && (
                      <div className="item-description">{item.description || item.item_description}</div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      );
    }
  };

  return (
    <div className={`message-bubble ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        {renderMessageContent()}
        <div className="message-time">
          {formatTime(timestamp)}
          {isUser && <span className="message-status">✓</span>}
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
