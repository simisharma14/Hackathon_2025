import React from 'react';
import './LandingPage.css'; // Import the CSS file
import { Link } from "react-router-dom"; // Import Link


const LandingPage = () => {
  return (
    <div className="landing-page">
      <div className="fullscreen-bg">
      <div className="fullscreen-overlay"></div>
      <div className="fullscreen-content">
      <div className="content-box">
          <h1 className="fade-in">Welcome to Green Thumb</h1>
          <p className="fade-in delay-1">
            Join us in investing towards a sustainable and renewable world.
          </p>
          <Link to="/Home">
          <button className="landing-page-start-button fade-in delay-2">
            Get Started
          </button>
          </Link>
        </div>
    </div>
    </div>
    </div>
  );
};

export default LandingPage;