import React, { useState, useRef } from 'react';
// import './ChatInterface.css';
import Sidebar from './Sidebar';
import ChatHistory from './ChatHistory';

const ChatInterface = () => {
  
    return (
    <div>
      <Sidebar />
      <ChatHistory />
    </div>
  );
};
export default ChatInterface;
