import React, { useState } from "react";

const promptContainerStyle = {
  width: "33.33%", // 1/3 of the screen width
  backgroundColor: "#FFDAB9", // Peach color
  padding: "20px",
  boxSizing: "border-box",
  borderRadius: "8px",
  boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
};

const inputStyle = {
  width: "100%",
  padding: "10px",
  marginBottom: "10px",
  border: "1px solid #ccc",
  borderRadius: "4px",
};

const buttonStyle = {
  padding: "10px 20px",
  backgroundColor: "#FFA07A", // Lighter shade of peach for button
  color: "#fff",
  border: "none",
  borderRadius: "4px",
  cursor: "pointer",
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
          // Clear the previous imageUrls before updating with new ones
          setImageUrls(responseData.imageFiles);
        } else {
          // If no images are returned, reset the imageUrls state to an empty array
          setImageUrls([]);
        }
      }
    } catch (error) {
      console.error("Error sending data to backend:", error);
    }
  };

  return (
    <div style={promptContainerStyle}>
      <h1> Enter a prompt for an outfit!</h1>
      <input
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        style={inputStyle}
      />
      <button type="button" onClick={sendDataToBackend} style={buttonStyle}>
        Submit
      </button>
      <div>
        {imageUrls.map((imageUrl) => (
          <img key={imageUrl} src={imageUrl} alt="" width="150" height="150" />
        ))}
      </div>
    </div>
  );
}
