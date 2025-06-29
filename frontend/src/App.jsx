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
    <div style={{ padding: '2rem' }}>
      <SearchBar onSearch={setQuery} />
      <ul>
        {results.map((item, idx) => (
          <li key={idx} style={{ padding: '0.5rem 0' }}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
