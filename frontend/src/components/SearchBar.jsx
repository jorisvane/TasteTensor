import React from 'react';
import './SearchBar.css';
import { FaSearch } from 'react-icons/fa';

export default function SearchBar({ onSearch }) {
  return (
    <div className="search-bar-wrapper">
      <span className="search-label">
        <span className="label-line">Taste</span>
        <span className="label-line">Tensor</span>
      </span>
      <div className="search-bar">
        <FaSearch className="search-icon" />
        <input
          type="text"
          placeholder="Type to search..."
          onChange={(e) => onSearch(e.target.value)}
        />
      </div>
    </div>
  );
}
