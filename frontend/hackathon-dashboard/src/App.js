import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Dashboard from "./dashboard"; // Import the Dashboard component
import LandingPage from "./LandingPage"; // Import the LandingPage component
import Home from ".//Home"; // Make sure Home is imported
import ETFPage from "./ETFPage"; // Make sure Home is imported
import TopPerformers from "./TopPerformers";
import ProfileViews from "./ProfileViews";
import StockProfile from "./StockProfile";
// import MacroOutlook from "./pages/MacroOutlook";
// import StockProfile from "./pages/StockProfile";
// import TopPerformers from "./pages/TopPerformers";

function App() {
  return (
    <Router>
      <div className="App">
        {/* Route Definitions */}
        <Routes>
          {/* Landing Page Route */}
          <Route path="/" element={<LandingPage />} />
          {/* Home Page Route */}
          <Route path="/home" element={<Home />} /> {/* Home page route */}
          {/* Dashboard Page Route */}
          <Route path="/dashboard" element={<Dashboard />} />
          {/* Top Performers Page Route */}
          <Route path="/TopPerformers" element={<TopPerformers />} />
          <Route path="/ETFPage" element={<ETFPage />} />
          <Route path="/ProfileViews" element={<ProfileViews />} />
          <Route path="/stock/:symbol" element={<StockProfile />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
