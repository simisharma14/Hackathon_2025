import { useState } from "react";
import "./Home.css";
import { Link } from "react-router-dom";
import { useGlobalContext } from "./GlobalContext";


const Home = () => {
    const { userData, setUserData } = useGlobalContext();

    return (
        <div className="home-bg">
            <div className="home-overlay"></div>

            {/* Title */}
            <h2 className="home-title fade-in">Please Enter Your Name and Stock Preferrences</h2>

            {/* Centered Form */}
            <div className="home-content">
                <div className="home-box">
                    {/* Name Entry Field */}
                    <input
                        type="text"
                        placeholder="Enter Your Name"
                        value={userData.name}
                        onChange={(e) => setUserData({ ...userData, name: e.target.value })}
                        className="home-input fade-in"
                    />

                    {/* Energy Type Dropdown */}
                    <select
                        value={userData.energyType}
                        onChange={(e) => setUserData({ ...userData, energyType: e.target.value })}
                        className={`home-dropdown fade-in delay-1 ${userData.energyType ? "" : "placeholder"}`}
                    >
                        <option value="" disabled hidden>Energy Type</option>
                        <option value="Wind">Wind</option>
                        <option value="Solar">Solar</option>
                        <option value="Nuclear">Nuclear</option>
                    </select>

                    {/* Risk Type Dropdown */}
                    <select
                        value={userData.riskType}
                        onChange={(e) => setUserData({ ...userData, riskType: e.target.value })}
                        className={`home-dropdown fade-in delay-2 ${userData.riskType ? "" : "placeholder"}`}
                    >
                        <option value="" disabled hidden>Risk Level</option>
                        <option value="Low">Low</option>
                        <option value="Moderate">Moderate</option>
                        <option value="High">High</option>
                    </select>

                    {/* Proceed Button */}
                    <button className="home-page-start-button fade-in delay-3">
                        Proceed
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Home;
