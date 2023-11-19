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

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = () => {
    alert(`You entered: ${inputValue}`);
  };

  return (
    <div style={promptContainerStyle}>
      <h2>Prompt</h2>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Enter something..."
        style={{ width: "100%", marginBottom: "10px" }}
      />
      <button type="button" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
}
