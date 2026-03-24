import { useEffect, useState } from "react";
import API from "./api";
import CreateURL from "./CreateURL";

function Dashboard() {
  const [urls, setUrls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchURLs();
  }, []);

  const fetchURLs = async () => {
    try {
      setLoading(true);
      const res = await API.get("/api/my-urls/");
      setUrls(res.data.results);
      setLoading(false);
    } catch (err) {
      console.log(err);
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>My URLs</h2>

      <CreateURL refresh={fetchURLs} />

      {loading ? (
        <p>Loading...</p>
      ) : (
        urls.map((url) => (
          <div key={url.id}>
            <p>{url.original_url}</p>
            <p>Clicks: {url.click_count}</p>

            <button
              onClick={() => {
                const fullURL = `http://127.0.0.1:8000/${url.short_code}`;
                navigator.clipboard.writeText(fullURL);
                alert("Copied!");
              }}
            >
              Copy Link
            </button>

            <hr />
          </div>
        ))
      )}
    </div>
  );
}

export default Dashboard;