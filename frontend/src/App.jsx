import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  useEffect(() => {
    if (!query) return;

    const fetchResults = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/search?query=${query}`);
        const data = await response.json();
        setResults(data.results);
      } catch (err) {
        console.error('Failed to fetch:', err);
      }
    };

    fetchResults();
  }, [query]);

  return (
    <div className="app-container">
      <div className="top-row">
        <div className="search-label">
          <span className="label-line">Taste</span>
          <span className="label-line">Tensor</span>
        </div>
        <div className="centered-search-bar">
          <SearchBar onSearch={setQuery} />
        </div>
      </div>

      <ul className="results-list">
        {results.map((item, idx) => (
          <li key={idx}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
