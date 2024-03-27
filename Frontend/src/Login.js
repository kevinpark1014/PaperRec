import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import './Login.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false); // 추가
  const { login } = useAuth();
  const navigate = useNavigate();
  // Remember Me 체크박스 변경 핸들러
  const handleRememberMeChange = () => {
    setRememberMe(!rememberMe);
  };
  useEffect(() => {
    // 페이지가 로드될 때 로컬 스토리지에서 이메일과 비밀번호를 가져와 설정합니다.
    const rememberedEmail = localStorage.getItem('rememberedEmail');
    const rememberedPassword = localStorage.getItem('rememberedPassword');
    if (rememberedEmail && rememberedPassword) {
      setUsername(rememberedEmail);
      setPassword(rememberedPassword);
      setRememberMe(true);
    }
  }, []);
  const handleSignUp = () => {
    navigate('/signup')
  };
  const handleLogin = async () => {
    try {
      const response = await axios.post(
        'http://175.45.201.130:8000/login',
        {
          username,
          password,
        },
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      // Handle successful login
      const { access_token, token_type } = response.data;
      login(response.data);

      if (rememberMe) {
        // Remember Me가 체크되어 있으면 이메일과 비밀번호를 로컬 스토리지에 저장
        localStorage.setItem('rememberedEmail', username);
        localStorage.setItem('rememberedPassword', password);
      } else {
        // Remember Me가 체크되어 있지 않으면 로컬 스토리지에서 저장된 이메일과 비밀번호 삭제
        localStorage.removeItem('rememberedEmail');
        localStorage.removeItem('rememberedPassword');
      }

      // Pass the token to the parent component or perform other actions
    } catch (error) {
      // Handle login failure
      console.error('Error logging in:', error);
    }
  };

  return (
    <div className="container">
      <div className="login-container">
        <h1 className='font_big'>ACCOUNT&nbsp;&nbsp;LOGIN</h1>
        <div>
          <h2 className='font_email'>E-mail</h2> 
          <input
            type="text"
            className="login-input"
            // placeholder="E-mail"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <h2 className='font_password'>Password</h2>
          <input
            type="password"
            className="login-input"
            // placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className='leftbox'>
          <input
            type="checkbox"
            id="rememberMeCheckbox"
            checked={rememberMe}
            onChange={handleRememberMeChange}
          />
          <label htmlFor="rememberMeCheckbox">Remember Me</label>
        </div>
        <button onClick={handleLogin} className="login-button">
          LOGIN
        </button>
      </div>
      <div className="sign-container">
          <label className='summary'>Enter your personal details and start journey with us</label>
          <button onClick={handleSignUp} className="sign-button">
          Sign Up
        </button>
      </div>
    </div>
  );
};

export default Login;