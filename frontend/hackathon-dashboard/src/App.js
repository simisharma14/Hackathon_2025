import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom"; 
import "./App.css";
import Dashboard from "./dashboard"; // Import the Dashboard component

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Links */}
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/dashboard">View Dashboard</Link>
            </li>
          </ul>
        </nav>

        {/* Route Definitions */}
        <Routes>
          {/* Home Page Route */}
          <Route path="/" element={<h1>Hello Simi and Jeslyn!</h1>} />

          {/* Dashboard Page Route */}
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
