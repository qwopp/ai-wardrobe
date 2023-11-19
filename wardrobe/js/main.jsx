import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import Clothes from "./clothes";
import Prompt from "./prompt";
import FileUpload from "./file_upload";

// Create a root

const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM
if (document.getElementById("indexComponent")) {
  root.render(
    <StrictMode>
      <div style={{ display: "flex", width: "100%" }}>
        <Clothes />
        <Prompt />
      </div>
    </StrictMode>
  );
} else {
  root.render(
    <StrictMode>
      <FileUpload />
    </StrictMode>
  );
}
console.log(root);
