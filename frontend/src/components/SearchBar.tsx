import React, { useState } from 'react';
import './SearchBar.css';
import { FaSearch } from 'react-icons/fa';
import { IconContext } from 'react-icons';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [input, setInput] = useState('');

  return (
    <div className="search-bar">
      <IconContext.Provider value={{ className: 'search-icon' }}>
        <FaSearch />
      </IconContext.Provider>
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