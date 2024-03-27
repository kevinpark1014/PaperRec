import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Navbar 스타일을 정의하는 CSS 파일을 import
import { useAuth } from './AuthContext';

const Navbar = () => {
  const { logout, token } = useAuth();
  const handleLogout = async () => {
    logout();
  }
  return (
    <div className="navbar">
        <div>
                <a href="/">
                    <img src="./logo_4.png" className='logo'/>
                    <h1 className='font_logo'>PRQAS</h1>
                </a>
        </div>
        {token ? (
        <div>
                <a href="/">
                 <button onClick={handleLogout} className='logout-button'>
                  Logout
                </button>
              </a>
        </div>
        ):(
          <div>
              <Link to="/login">
                  <div className='signinup-button'>
                    Sign in/Sign up
                  </div>
                </Link>
          </div>
          )}
    </div>
  );
};

export default Navbar;