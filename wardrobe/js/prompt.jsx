// prompt.jsx
import React, { useState } from "react";

const promptContainerStyle = {
  width: "33.33%", // 1/3 of the screen width
  backgroundColor: "#f0f0f0",
  padding: "20px",
  boxSizing: "border-box",
};

export default function Prompt() {
  const [inputValue, setInputValue] = useState("");
  const [imageUrls, setImageUrls] = useState([]);

  const sendDataToBackend = async () => {
    try {
      const response = await fetch("/api/v1/prompt/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ inputData: inputValue }),
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log("Received response from backend:", responseData);
        if (responseData.imageFiles && responseData.imageFiles.length > 0) {
          setImageUrls(responseData.imageFiles);
        }
      }
    } catch (error) {
      console.error("Error sending data to backend:", error);
    }
  };

  return (
    <div style={promptContainerStyle}>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <button type="button" onClick={sendDataToBackend}>
        Submit
      </button>

      <div>
        {imageUrls.map((imageUrl, index) => (
          <img key={index} src={imageUrl} alt="" />
        ))}
      </div>
    </div>
  );
}