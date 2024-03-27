import './App.css';
import React from 'react';
// import ChatInterface from './ChatInterface';
import User from './User';
import Navbar from './Navbar';
import Search from './Search';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './Login';
import SignUp from './SignUp';
import Main from './Main';
import { AuthProvider } from './AuthContext';
import ChatInterface from './ChatInterface';
function App() {
  return (
    <BrowserRouter>
    <AuthProvider>
      <div className="App">
        <Navbar />
        <Routes>
        <Route path="/" element={<Search />} />
        <Route path="/chat" element={<ChatInterface />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/user" element={<User />} />

        </Routes>
      </div>
      </AuthProvider>
    </BrowserRouter>
);
}

export default App;
