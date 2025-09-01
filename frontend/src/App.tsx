import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import RecipeMap from './components/RecipeMap'; 
import './App.css';

interface SearchResult {
  title: string;
  image: string;
  x: number;
  y: number;
}

interface Coords {
  x: number;
  y: number;
}

interface ApiResponse {
  results: SearchResult[];
  queryCoords: Coords | null;
}

function App() {
  const [query, setQuery] = useState<string>('');
  const [apiResponse, setApiResponse] = useState<ApiResponse>({
    results: [],
    queryCoords: null,
  });

  useEffect(() => {
    if (!query) return;

    const fetchResults = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/search?query=${query}`);
        const data: ApiResponse = await response.json();
        setApiResponse(data); 
      } catch (err) {
        console.error('Failed to fetch:', err);
      }
    };

    fetchResults();
  }, [query]);

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo">
          TasteTensor
        </div>
        <div className="search-bar-container">
          <SearchBar onSearch={setQuery} />
        </div>
      </header>

     <main className="map-view-container">
      {apiResponse.results.length > 0 && apiResponse.queryCoords && (
        <RecipeMap
          recipes={apiResponse.results}
          queryCoords={apiResponse.queryCoords}
        />
      )}
    </main> 
    </div>
  );
}

export default App;