import React, { useState } from "react";

function App() {
  const [name, setName] = useState("");
  const [greeting, setGreeting] = useState("");
  const [error, setError] = useState("");

  const backendUrl = "https://greet-ahu2xfbthq-uc.a.run.app";

  async function handleSubmit(event) {
    event.preventDefault(); // Prevent full page reload

    setGreeting("");
    setError("");

    if (!name.trim()) {
      setError("Please enter your name.");
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/greet?name=${encodeURIComponent(name)}`);
      const data = await response.json();

      if (response.ok) {
        setGreeting(data.message);
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    }
  }

  return (
    <div>
      <h1>Greet App</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={name}
          onChange={e => setName(e.target.value)}
          placeholder="Enter your name"
        />
        <button type="submit">Greet Me</button>
      </form>
      {greeting && <p>{greeting}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default App;
