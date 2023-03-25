import { useState } from 'react';
import axios from 'axios';
import PdfUploader from "../components/PdfUploader"
import Head from 'next/head';
import Input from '@material-tailwind/react/components/Input';

export default function Home() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = async () => {
    if (!query) return;
    try {
      const response = await axios.get('http://localhost:5000/search', { params: { query } });
      setSearchResults(response.data);
      console.log(response.data)
    } catch (error) {
      alert('Error searching the index.');
    }
  };

  

  return (
    <>
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <Head>
        <title>Alexandria</title>
        <meta
          name="description"
          content="A simple PDF search engine built using Python, Flask, Whoosh, and Next.js"
        />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <h1 className="text-4xl font-semibold text-center text-gray-800 mb-4">
          Project_Alexandria: Search Engine
        </h1>
        <h2 className="text-2xl font-semibold text-center text-gray-600 mb-4">
          Upload PDF or enter a PDF URL
        </h2>

        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <PdfUploader />
          <div className="mb-4 w-72">
            <Input
              type="text"
              value={query}
              label="Search Alexandria"
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          <button
            onClick={handleSearch}
            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Search
          </button>
          <h2 className="text-2xl font-semibold text-center text-gray-600 mt-8 mb-4">
            Results
          </h2>
          <ul className="list-disc list-inside">
            {searchResults.map((result, index) => (
              <li key={index} className="text-gray-700 text-lg mb-2">
                {result[0]} <span className="text-gray-500">(score: {result[1]})</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
    </>
    // <>
    //   <Head>
    //     <title>PDF Search Engine</title>
    //     <meta name="description" content="A simple PDF search engine built using Python, Flask, Whoosh, and Next.js" />
    //     <link rel="icon" href="/favicon.ico" />
    //   </Head>
    //   <h1>PDF Search Engine</h1>
    //   <h2>Upload PDF</h2>
      
    //   <PdfUploader/>
    //   <div className="w-72">
    //     <Input 
    //     type="text"
    //     value={query}
    //     label="Search Alexandria" 
    //     onChange={(e) => setQuery(e.target.value)}
    //     />
    //   </div>
    //   <button onClick={handleSearch}>Search</button>
    //   <h2>Results</h2>
    //   <ul>
    //     {searchResults.map((result, index) => (
    //       <li key={index}>
    //         {result[0]} (score: {result[1]})
    //       </li>
    //     ))}
    //   </ul>

    // </>
  );
}
