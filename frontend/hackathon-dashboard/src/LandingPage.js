import React from "react";
import { Link } from "react-router-dom"; // Import Link

function LandingPage() {
  return (
    <div className="landing-page">
      <h1>Welcome to Green Thumb!</h1>
      <p>Our Problem Statement</p>
      <p>We aim to...lallaala</p>
      {/* Link to Home page */}
      <Link to="/home">
        <button>Get Started</button>
      </Link>
    </div>
  );
}

export default LandingPage;
