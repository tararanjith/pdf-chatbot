// src/App.js
import React, { useState } from 'react';
import UploadSection from './components/UploadSection';
import ChatSection from './components/ChatSection';

const App = () => {
  const [uploaded, setUploaded] = useState(false);

  const handleUploadSuccess = () => {
    setUploaded(true);
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-8 gap-8">
      {!uploaded ? (
        <UploadSection onUpload={handleUploadSuccess} />

      ) : (
        <ChatSection />
      )}
    </div>
  );
};

export default App;
