import React, { useState } from "react";
import axios from "axios";

const PDFUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    try {
      await axios.post("http://localhost:5000/upload", formData);
      alert("Upload successful!");
      onUploadSuccess();
    } catch (err) {
      alert("Upload failed.");
    }
    setUploading(false);
  };

  return (
    <div className="pdf-upload">
      <input
        type="file"
        accept="application/pdf"
        onChange={e => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload PDF"}
      </button>
    </div>
  );
};

export default PDFUpload;
