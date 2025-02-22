import React from 'react';
import './StockProfile.css'; // Import the CSS file
import { Link } from "react-router-dom"; // Import Link

const StockProfile = () => {
    return (
      <div className="stockprofile">
        <h1>NAME ENTRY!</h1>
        <p>ENERGY TYPE</p>
        <p>RISK TYPE</p>

        <Link to="/dashboard">
              <button class="stock-profile-start-button"> See Stock Profile!</button>
        </Link>
      </div>
    );
  };
  
  export default StockProfile;
  