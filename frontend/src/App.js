import { useState } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div style={{ maxWidth: "500px", margin: "auto" }}>
      {token ? (
        <>
          <button onClick={handleLogout}>Logout</button>
          <Dashboard />
        </>
      ) : (
        <Login setToken={setToken} />
      )}
    </div>
  );
}

export default App;