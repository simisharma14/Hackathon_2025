import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom"; 
import Layout from "./components/Layout";
import "./App.css";
import Dashboard from "./dashboard"; // Import the Dashboard component
import Home from "./pages/Home";
import MacroOutlook from "./pages/MacroOutlook";
import StockProfile from "./pages/StockProfile"
import TopPerformers from "./pages/TopPerformers";

function App() {
  return (
    <Router>
      <Layout>
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
      </Layout>
    </Router>
  );
}

export default App;
