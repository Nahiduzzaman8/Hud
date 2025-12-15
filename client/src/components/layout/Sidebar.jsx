// src/components/layout/Sidebar.jsx
import { useEffect, useState } from "react";

const FIXED_CATEGORIES = [
  "Technology",
  "Politics",
  "Business",
  "Sports",
  "Football",
  "Badminton",
  "Health",
];

function Sidebar({ onLogout }) {
  const [preferences, setPreferences] = useState([]);
  const [category, setCategory] = useState("");
  const [topics, setTopics] = useState("");

  // GET preferences
  const fetchPreferences = async () => {
    const res = await fetch("http://localhost:8000/preferences", {
      credentials: "include",
    });

    if (res.status === 401) {
      window.location.href = "/login";
      return;
    }

    const result = await res.json();
    if (result.success) {
      setPreferences(result.data);
    }
  };

  useEffect(() => {
    fetchPreferences();
  }, []);

  // ADD preference
  const handleAdd = async () => {
    if (!category || !topics) return;

    await fetch("http://localhost:8000/preferences/add/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        category: category,
        topics: topics, // backend expects "topics"
      }),
    });

    setTopics("");
    fetchPreferences();
  };

  // DELETE single
  const handleDelete = async (id) => {
    await fetch("http://localhost:8000/preferences/delete/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ id }),
    });

    fetchPreferences();
  };

  // DELETE all
  const handleDeleteAll = async () => {
    await fetch("http://localhost:8000/preferences/delete-all/", {
      method: "POST",
      credentials: "include",
    });

    fetchPreferences();
  };

  // LOGOUT
  const handleLogout = async () => {
    await fetch("http://localhost:8000/logout/", {
      method: "POST",
      credentials: "include",
    });

    onLogout();
  };

  return (
    <div className="w-72 bg-white border-r min-h-screen flex flex-col p-4">

      {/* Title */}
      <h3 className="text-lg font-semibold mb-4">Preferences</h3>

      {/* Category + Topics */}
      <div className="flex gap-2 mb-3">
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="w-1/2 p-2 border rounded-lg"
        >
          <option value="">Category</option>
          {FIXED_CATEGORIES.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Topics"
          value={topics}
          onChange={(e) => setTopics(e.target.value)}
          className="w-1/2 p-2 border rounded-lg"
        />
      </div>

      <button
        onClick={handleAdd}
        className="mb-3 bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600"
      >
        Add
      </button>

      {/* Reload + Delete All */}
      <div className="flex gap-2 mb-4">
        <button
          onClick={fetchPreferences}
          className="w-1/2 border p-2 rounded-lg"
        >
          Reload
        </button>

        <button
          onClick={handleDeleteAll}
          className="w-1/2 bg-red-500 text-white p-2 rounded-lg hover:bg-red-600"
        >
          Delete All
        </button>
      </div>

      {/* Preferences List */}
      <div className="flex-1 space-y-2 overflow-y-auto">
        {preferences.map((pref) => (
          <div
            key={pref.id}
            className="flex justify-between items-center bg-gray-100 p-2 rounded-lg text-sm"
          >
            <span>
              {pref.category} — {pref.topics}
            </span>
            <button
              onClick={() => handleDelete(pref.id)}
              className="text-red-500 hover:underline"
            >
              Delete
            </button>
          </div>
        ))}
      </div>

      {/* Logout */}
      <button
        onClick={handleLogout}
        className="mt-4 bg-gray-800 text-white p-2 rounded-lg hover:bg-black"
      >
        Logout
      </button>
    </div>
  );
}

export default Sidebar;
