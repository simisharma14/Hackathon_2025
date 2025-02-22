import React from 'react';
import './LandingPage.css'; // Import the CSS file
import { Link } from "react-router-dom"; // Import Link

const LandingPage = () => {
  return (
    <div className="landing-page">
      <h1>Welcome to Green Thumb!</h1>
      <p>Our Problem Statement</p>
      <p> Here at Green Thumb we... lallalalallal</p>
      <Link to="/home">
      <button class="landing-page-start-button"> Get Started!</button>
      </Link>
    </div>
  );
};

export default LandingPage;