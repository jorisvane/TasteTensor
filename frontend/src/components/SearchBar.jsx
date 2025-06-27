import React from 'react';

export default function SearchBar({ onSearch }) {
  return (
    <input
      type="text"
      placeholder="Search..."
      onChange={(e) => onSearch(e.target.value)}
      className="border p-2 w-full max-w-md"
    />
  );
}
