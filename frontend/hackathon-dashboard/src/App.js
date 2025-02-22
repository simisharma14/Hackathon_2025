import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom"; 
import Layout from "./components/Layout";
import "./App.css";
import Dashboard from "./dashboard"; // Import the Dashboard component
import LandingPage from "./LandingPage"; // Import the LandingPage component
// import Home from "./pages/Home";
// import MacroOutlook from "./pages/MacroOutlook";
// import StockProfile from "./pages/StockProfile";
// import TopPerformers from "./pages/TopPerformers";

function App() {
  return (
    <Router>
      <Layout>
        <div className="App">
          {/* Navigation Links */}
          <nav>
            <ul>
              <li>
                <Link to="/">LandingPage</Link>
              </li>
              <li>
                <Link to="/dashboard">View Dashboard</Link>
              </li>
            </ul>
          </nav>

          {/* Route Definitions */}
          <Routes>
            {/* Landing Page Route */}
            <Route path="/" element={<LandingPage />} />

            {/* Dashboard Page Route */}
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </Layout>
    </Router>
  );
}

export default App;
