// src/components/layout/Topbar.jsx
function Topbar() {
  return (
    <div className="h-14 bg-white border-b flex items-center justify-between px-6">
      
      {/* App Name */}
      <h1 className="text-xl font-semibold">MyDashboard</h1>

      {/* Search */}
      <input
        type="text"
        placeholder="Search..."
        className="w-64 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
      />
    </div>
  );
}

export default Topbar;
