import React, { createContext, useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate();
  const [token, setToken] = useState(() => {
    const storedToken = localStorage.getItem('accessToken');
    return storedToken ? JSON.parse(storedToken) : null;
  });
  const login = (newToken) => {
    setToken(newToken);
    localStorage.setItem('accessToken', JSON.stringify(newToken));
    navigate('/');
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('accessToken');
    navigate('/');
  };

  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return useContext(AuthContext);
};