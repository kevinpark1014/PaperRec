import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const Search = () => {
  const [keyword, setKeyword] = useState('');
  const [searchResult, setSearchResult] = useState('');
  const { token } = useAuth();
  const accessToken = token;

  const handleSearch = async (token_1) => {
    try {
      // POST request: Send keyword to server
      await axios.post('http://175.45.201.130:8000/keyword', { 'content' : keyword }, {
        headers: {
          Authorization: `Bearer ${token_1}`,
        },});

      // GET request: Fetch search results
      const response = await axios.get(`http://175.45.201.130:8000/keyword/${keyword}`, {
        headers: {
          Authorization: `Bearer ${token_1}`,
        },});
        
      setSearchResult(response.data);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        placeholder="Enter keyword"
      />
      <button onClick={() => handleSearch(token.access_token)}>Search</button>

      {searchResult && (
        <div>
          {/* Display search results */}
          <h2>Search Results</h2>
          <ul>
            {searchResult.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Search;
