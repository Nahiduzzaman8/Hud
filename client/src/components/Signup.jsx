import { useState } from "react";

function Signup({ onLoginRedirect }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/signup/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include", // important for cookie
        body: JSON.stringify({ username, email, password }),
      });

      const data = await res.json();
      if (data.success) {
        alert("Signup successful! You can now login.");
        onLoginRedirect();
      } else {
        alert(data.message);
      }
    } catch (err) {
      console.error(err);
      alert("Signup failed.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 px-4">
      <div className="bg-white shadow-lg rounded-2xl p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-6 text-center">Create Account</h2>
        
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-3 mb-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 mb-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 mb-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <button
          onClick={handleSignup}
          className="w-full bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600 transition-colors mb-4"
        >
          Sign Up
        </button>

        <div className="text-center text-sm text-gray-500 mb-4">
          Already have an account?{" "}
          <span
            onClick={onLoginRedirect}
            className="text-blue-500 hover:underline cursor-pointer"
          >
            Login
          </span>
        </div>

        <div className="flex items-center justify-center mb-2">
          <span className="border-b w-full border-gray-300"></span>
          <span className="px-2 text-gray-400">or</span>
          <span className="border-b w-full border-gray-300"></span>
        </div>

        <button className="w-full flex items-center justify-center gap-2 p-3 border rounded-lg hover:bg-gray-100 transition-colors">
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
            alt="Google"
            className="w-5 h-5"
          />
          Login with Google
        </button>
      </div>
    </div>
  );
}

export default Signup;
