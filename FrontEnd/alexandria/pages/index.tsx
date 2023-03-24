import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleFileChange = (e: any) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post('http://localhost:5000/upload', formData);
      alert(response.data.message);
    } catch (error) {
      alert('Error uploading the file.');
    }
  };

  const handleSearch = async () => {
    if (!query) return;
    try {
      const response = await axios.get('http://localhost:5000/search', { params: { query } });
      setSearchResults(response.data);
    } catch (error) {
      alert('Error searching the index.');
    }
  };

  return (
    <div>
      <h1>PDF Search Engine</h1>
      <h2>Upload PDF</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <h2>Search</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter search query"
      />
      <button onClick={handleSearch}>Search</button>
      <h2>Results</h2>
      <ul>
        {searchResults.map((result, index) => (
          <li key={index}>
            {result[0]} (score: {result[1]})
          </li>
        ))}
      </ul>
    </div>
  );
}
