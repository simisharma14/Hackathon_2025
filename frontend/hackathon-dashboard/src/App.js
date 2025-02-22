import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; 
import Layout from "./components/Layout";
import "./App.css";
import Dashboard from "./dashboard"; // Import the Dashboard component
import LandingPage from "./LandingPage"; // Import the LandingPage component
import Home from ".//Home"; // Make sure Home is imported
// import MacroOutlook from "./pages/MacroOutlook";
// import StockProfile from "./pages/StockProfile";
// import TopPerformers from "./pages/TopPerformers";

function App() {
  return (
    <Router>
      <Layout>
        <div className="App">
          {/* Route Definitions */}
          <Routes>
            {/* Landing Page Route */}
            <Route path="/" element={<LandingPage />} />

            {/* Home Page Route */}
            <Route path="/home" element={<Home />} /> {/* Home page route */}

            {/* Dashboard Page Route */}
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </Layout>
    </Router>
  );
}

export default App;
