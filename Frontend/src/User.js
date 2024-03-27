import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const User = () => {
  const [userData, setUserData] = useState(null);
  const { logout, token } = useAuth();
  useEffect(() => {
    // localStorage에서 토큰을 가져옴
    const accessToken = token;
    // 토큰이 있다면 사용자 정보를 가져옴
    if (accessToken) {
      fetchUserData(accessToken.access_token);
    }
  }, []);
  const fetchUserData = async (token_1) => {
    try {
      // 토큰을 헤더에 포함시켜서 요청을 보냄
      const response = await axios.get('http://175.45.201.130:8000/user/', {
        headers: {
          Authorization: `Bearer ${token_1}`,
        },
      });
      // console.log(response.data)
      // 사용자 정보를 상태에 저장
      setUserData(response.data);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  return (
    <div>
      <h2>Welcome to the Home Page</h2>
      {userData ? (
        <div>
          <p>User ID: {userData.user_id}</p>
          <p>Email: {userData.email}</p>
          {/* 기타 사용자 정보 표시 */}
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
};

export default User;