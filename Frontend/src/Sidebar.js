import React from 'react';

const Sidebar = () => {
    const navbarHeight = 80;
  return (
    <div style={{ width: '20%', backgroundColor: '#e0e0e0', height: `calc(100vh - ${navbarHeight}px)`, float: 'left',overflowY: 'auto' }}>
      {/* Sidebar content */}
      <h2>Chat Room List</h2>
      {/* Add chat room list items here */}
    </div>
  );
};

export default Sidebar;