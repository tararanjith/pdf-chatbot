// src/components/UploadSection.js
import React, { useState } from 'react';
import axios from 'axios';

const UploadSection = ({ onUpload }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('pdf', file); // 👈 This must match backend: request.files.get('pdf')

    setUploading(true);
    try {
      const res = await axios.post('http://127.0.0.1:5000/upload', formData, {

        headers: { 'Content-Type': 'multipart/form-data' },
        withCredentials: true,
      });

      console.log('Upload response:', res.data);
      onUpload(); // Trigger success state
    } catch (err) {
      console.error('Upload error:', err.response?.data || err.message);
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 bg-zinc-800 text-white rounded-lg shadow-md w-full max-w-md text-center">
      <h2 className="text-xl font-semibold mb-4">Upload your PDF</h2>
      <input type="file" onChange={handleFileChange} className="mb-4 w-full text-white" />
      <button
        onClick={handleUpload}
        disabled={uploading}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      {error && <p className="text-red-400 mt-2">{error}</p>}
    </div>
  );
};

export default UploadSection;
