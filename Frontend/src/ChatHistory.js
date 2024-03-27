import React from 'react';

const ChatHistory = () => {
    const navbarHeight = 80;
    // paper_id를 입력받으면 
    // 1. Usermessage와 Chatmessage를 구분하는 도구 -> Usermessage이면 표현 Chatmessage면 이렇게 표현
    // 1-1. 표현할 때, Username이 들어가고 한칸 띄고 PRQAS 들어가게끔
    // 2. 스크롤 가능하게끔 하는 거


    return (
    <div style={{ width: '80%', backgroundColor: '#f0f0f0', height: `calc(100vh - ${navbarHeight}px)`, float: 'left', overflowY: 'auto' }}>
      {/* Chat history content */}
      <h2>Chat History</h2>
      {/* Display chat history here */}
    </div>
  );
};

export default ChatHistory;