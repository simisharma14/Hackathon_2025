import React from 'react';
import './Home.css'; // Import the CSS file
import { Link } from "react-router-dom"; // Import Link

const Home = () => {
    return (
      <div className="home">
        <h1>NAME ENTRY!</h1>
        <p>ENERGY TYPE Choices</p>
        <p>RISK TYPE</p>

        {/* Link to Top Performers page */}
        <Link to="/ETFPage">
          <button className="home-page-start-button">View ETF Breakdown</button>
        </Link>
      </div>
    );
};

export default Home;
