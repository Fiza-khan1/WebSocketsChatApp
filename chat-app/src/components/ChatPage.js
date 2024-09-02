// src/components/ChatPage.js

import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const ChatPage = () => {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [typingStatus, setTypingStatus] = useState('');
  const [onlineUsers, setOnlineUsers] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    const ws = new WebSocket(`ws://127.0.0.1:8001/ws/chat/new/?token=${token}`);

    ws.onopen = () => {
      console.log('WebSocket connection established');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        setMessages((prevMessages) => [...prevMessages, { message: data.message, username: data.username }]);
      }
      if (data.typing) {
        setTypingStatus(`${data.username} is typing...`);
        setTimeout(() => setTypingStatus(''), 3000); // Clear typing status after 3 seconds
      }
      if (data.user_status) {
        const { username, status } = data.user_status;
        setOnlineUsers((prevUsers) => ({
          ...prevUsers,
          [username]: status
        }));
      }
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  const sendMessage = () => {
    if (socket) {
      socket.send(JSON.stringify({ message }));
      setMessage('');
    }
  };

  const handleTyping = () => {
    if (socket) {
      socket.send(JSON.stringify({ typing: true }));
    }
  };

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Chat</h2>
      <div className="row">
        <div className="col-md-8">
          <div className="border rounded p-3 bg-light">
            <div className="messages mb-3" style={{ maxHeight: '400px', overflowY: 'scroll' }}>
              {messages.map((msg, index) => (
                <div key={index} className="mb-2">
                  <strong>{msg.username}:</strong> {msg.message}
                </div>
              ))}
              {typingStatus && (
                <div className="text-muted">{typingStatus}</div>
              )}
            </div>
            <div className="input-group">
              <input
                type="text"
                className="form-control"
                value={message}
                onChange={(e) => {
                  setMessage(e.target.value);
                  handleTyping();
                }}
              />
              <button className="btn btn-primary" onClick={sendMessage}>Send</button>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="border rounded p-3 bg-light">
            <h4 className="mb-3">Online Users</h4>
            <ul className="list-group">
              {Object.entries(onlineUsers).map(([username, status]) => (
                <li key={username} className="list-group-item">
                  {username} <span className={`badge bg-${status === 'online' ? 'success' : 'secondary'}`}>{status}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
