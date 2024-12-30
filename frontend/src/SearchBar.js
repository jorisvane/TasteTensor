import React, { useState } from "react";
import axios from "axios";

const SearchBar = () => {
    const [query, setQuery] = useState(""); // For the input value
    const [response, setResponse] = useState(null); // To store the API response

    const handleSearch = async (e) => {
        e.preventDefault(); // Prevent page reload on form submit

        try {
            // Make POST request to backend
            const result = await axios.post(
                "http://127.0.0.1:8000/search",
                new URLSearchParams({ query }) // Use URLSearchParams for Form data
            );
            setResponse(result.data.message); // Update response state with API result
        } catch (error) {
            console.error("Error during search:", error);
            setResponse("An error occurred. Please try again.");
        }
    };

    return (
        <div style={{ margin: "2rem" }}>
            <h1>Search Ingredients</h1>
            <form onSubmit={handleSearch}>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your query"
                    style={{ padding: "0.5rem", width: "300px" }}
                />
                <button type="submit" style={{ marginLeft: "0.5rem", padding: "0.5rem" }}>
                    Search
                </button>
            </form>
            {response && (
                <div style={{ marginTop: "1rem", whiteSpace: "pre-wrap" }}>
                    <strong>Response:</strong>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
};

export default SearchBar;
