import React, { useState } from "react";

export default function FileUpload() {
  const [files, setFiles] = useState([]);

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles([...files, ...droppedFiles]);
  };

  const handleInputChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles([...files, ...selectedFiles]);
  };

  const handleUpload = () => {
    // Implement your file upload logic here using the 'files' state
    // For instance, send 'files' to an API endpoint
    console.log("Uploading files:", files);
    // Reset files state after uploading
    setFiles([]);
  };

  return (
    <div
      style={{
        border: "2px dashed #aaa",
        borderRadius: "5px",
        padding: "20px",
        textAlign: "center",
      }}
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <input
        type="file"
        multiple
        style={{ display: "none" }}
        onChange={handleInputChange}
        ref={(fileInput) => (this.fileInput = fileInput)}
      />
      <p>Drag and drop files here or</p>
      <button onClick={() => this.fileInput.click()}>Select Files</button>
      <button onClick={handleUpload}>Upload</button>

      {files.length > 0 && (
        <div style={{ marginTop: "20px" }}>
          <h4>Files to upload:</h4>
          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
