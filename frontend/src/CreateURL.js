import { useState } from "react";
import API from "./api";

function CreateURL({ refresh }) {
  const [originalURL, setOriginalURL] = useState("");
  const [customCode, setCustomCode] = useState("");
  const [shortURL, setShortURL] = useState("");

  const handleCreate = async () => {
    try {
      const res = await API.post("/api/shorten/", {
        original_url: originalURL,
        custom_code: customCode || undefined,
      });

      setShortURL(res.data.short_url);
      setOriginalURL("");
      setCustomCode("");
      refresh();
    } catch (err) {
      alert(err.response?.data?.detail || "Error creating URL");
    }
  };

  return (
    <div>
      <h3>Create Short URL</h3>

      <input
        type="text"
        placeholder="Enter URL"
        value={originalURL}
        onChange={(e) => setOriginalURL(e.target.value)}
      />

      <br /><br />

      <input
        type="text"
        placeholder="Custom code (optional)"
        value={customCode}
        onChange={(e) => setCustomCode(e.target.value)}
      />

      <br /><br />

      <button onClick={handleCreate}>Shorten</button>

      {shortURL && (
        <div>
          <p>Short URL:</p>
          <a href={shortURL} target="_blank" rel="noreferrer">
            {shortURL}
          </a>
        </div>
      )}
    </div>
  );
}

export default CreateURL;