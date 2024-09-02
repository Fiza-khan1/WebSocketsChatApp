// src/App.js

import React, { useState } from 'react';
import LoginPage from './components/LoginPage';
import ChatPage from './components/ChatPage'; // Assume you have a ChatPage component

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  return (
    <div>
      {isAuthenticated ? (
        <ChatPage />
      ) : (
        <LoginPage onLogin={handleLogin} />
      )}
    </div>
  );
};

export default App;
