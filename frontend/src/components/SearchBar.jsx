import React, { useState } from 'react';
import './SearchBar.css';
import { FaSearch } from 'react-icons/fa';

export default function SearchBar({ onSearch }) {

  const [input, setInput] = useState('');

  return (
    <div className="search-bar">
      <FaSearch className="search-icon" />
      <input
        type="text"
        placeholder="Type to search and enter..."
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            onSearch(input);
          }
        }}
      />
    </div>
  );
}
