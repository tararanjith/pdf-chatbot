import React, { useState } from "react";
import axios from "axios";

const PDFUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("pdf", file); // ✅ Match Flask's expected key

    setUploading(true);
    try {
      const res = await axios.post("http://localhost:5000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        withCredentials: true, // ✅ Required for Flask session
      });

      console.log("Upload response:", res.data);
      alert("Upload successful!");
      onUploadSuccess();
    } catch (err) {
      console.error("Upload failed:", err);
      alert("Upload failed. Please check the console for more details.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="pdf-upload">
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload PDF"}
      </button>
    </div>
  );
};

export default PDFUpload;
