import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";

const fileTypes = ["JPG", "PNG"];

function DragDrop() {
  const [file, setFile] = useState(null);

  const handleFileUpload = async () => {
    if (!file) {
      console.log("No file selected.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/v1/upload/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        console.log("File uploaded successfully!");
        // Perform actions after successful upload
      } else {
        console.error("Failed to upload file.");
        // Handle error scenarios
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      // Handle other errors
    }
  };

  const handleFileChange = (uploadedFile) => {
    setFile(uploadedFile);
  };

  return (
    <div>
      <FileUploader
        handleChange={handleFileChange}
        name="file"
        types={fileTypes}
      />
      <button type="button" onClick={handleFileUpload}>
        Upload File
      </button>
    </div>
  );
}

export default DragDrop;
