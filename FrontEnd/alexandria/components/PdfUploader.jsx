// components/PdfUploader.js
import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '../pages/api/upload';
import LoadingProgressBar from './LoadingProgressBar';
import Progress from '@material-tailwind/react/components/Progress';
import Button from '@material-tailwind/react/components/Button';
import {
  CloudArrowUpIcon,
} from "@heroicons/react/24/outline";


const PdfUploader = () => {
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [progress, setProgress] = useState(0);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const [loading, setLoading] = useState(false);

  const handleFileUpload = async () => {
    try {
      if (!file) {
        alert("Please choose a file to upload.");
        return;
      }
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(API_URL + "/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setProgress(percentCompleted);
        },
      });
      
      if (response.data.status === "success") {
        alert("File indexed.");
      } else {
        alert(response.data.message);
      }
      console.log("File upload response:", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file.");
    }
  };

  const handleUrlUpload = async () => {
    try {
      if (!url) {
        alert("Please enter a URL.");
        return;
      }
      setLoading(true);
      const response = await axios.post(
        API_URL + "/upload",
        { url },
        {
          headers: {
            "Content-Type": "application/json",
          },
          onUploadProgress: (progressEvent) => {
            
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(percentCompleted);
          },
        }
      );
      if (response.data.status === "success") {
        alert("File indexed.");
      } else {
        alert(response.data.message);
      }
      console.log("URL upload response:", response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file.");
    }
  };

  return (
    <div>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      {/* <button onClick={handleFileUpload}>Upload PDF</button> */}
      <Button variant="gradient" className="flex items-center gap-3" onClick={handleFileChange}>
        <CloudArrowUpIcon strokeWidth={2} className="h-5 w-5" /> Upload Files
      </Button>
      
      <input
        type="url"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter a PDF URL"
      />
      {/* <button onClick={handleUrlUpload}>Upload PDF from URL</button> */}
      <Button variant="gradient" className="flex items-center gap-3" onClick={handleUrlUpload}>
        <CloudArrowUpIcon strokeWidth={2} className="h-5 w-5" /> Submit URL
      </Button>
      <div>
        <LoadingProgressBar progress={progress} />
      </div>
    </div>
  );
};

export default PdfUploader;
