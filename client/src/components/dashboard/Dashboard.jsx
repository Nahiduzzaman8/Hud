// src/components/dashboard/Dashboard.jsx
import Sidebar from "../layout/Sidebar";
import Topbar from "../layout/Topbar";

function Dashboard() {
  const handleLogout = async () => {
    await fetch("http://localhost:8000/logout/", {
      method: "POST",
      credentials: "include",
    });
    window.location.href = "/login";
  };

  return (
    <div className="flex">
      <Sidebar username="nahid@example.com" onLogout={handleLogout} />

      <div className="flex-1">
        <Topbar />

        {/* Main section will go here */}
        <div className="p-6">
          <p className="text-gray-500">
            Carousel section will be implemented next.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
