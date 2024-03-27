import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignUp.css';

const SignUp = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const navigate = useNavigate();
  const handleSignUp = async () => {
    try {
      const response = await axios.post('http://175.45.201.130:8000/signup', {
        email,
        password,
        username
      });

      // Handle successful signup
      navigate('/login');
    } catch (error) {
      // Handle signup failure
      console.error('Error signing up:', error);
    }
  };

  return (
    <div className='container'>
      <div className='signup-container'>
        <h1 className='font_label'>Create Account</h1>
        <input 
          type="email" 
          className="sign-input" 
          value={email} 
          placeholder='E-mail'
          onChange={(e) => setEmail(e.target.value)} />
        <input 
          type="password" 
          className="sign-input" 
          value={password} 
          placeholder='Password'
          onChange={(e) => setPassword(e.target.value)} />
        <input 
          type="text" 
          className="sign-input" 
          value={username} 
          placeholder='Username'
          onChange={(e) => setUsername(e.target.value)} />
        <button className= 'signup-button' onClick={handleSignUp}>Sign Up</button>
      </div>
    </div>
  );
};

export default SignUp;