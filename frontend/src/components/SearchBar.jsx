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
        placeholder="Type to search..."
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            onSearch(input);
          }
        }}
      />
      <button onClick={() => onSearch(input)} className="search-button">
        Search
      </button>
    </div>
  );
}
