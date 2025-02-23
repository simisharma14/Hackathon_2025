import React from "react";
import { Link } from "react-router-dom";
import { useGlobalContext } from "./GlobalContext"; // Ensure this context is defined
import "./LandingPage.css";

const LandingPage = () => {
  const { userData, setUserData } = useGlobalContext();

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
            {/* Name Entry Field */}
            <input
              type="text"
              placeholder="Enter Your Name"
              value={userData.name}
              onChange={(e) =>
                setUserData({ ...userData, name: e.target.value })
              }
              className="landing-input fade-in"
            />
            {/* Risk Tolerance Dropdown */}
            <select
              value={userData.riskTolerance || ""}
              onChange={(e) =>
                setUserData({ ...userData, riskTolerance: e.target.value })
              }
              className="landing-dropdown fade-in delay-1"
            >
              <option value="" disabled>
                Select Risk Tolerance
              </option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
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
