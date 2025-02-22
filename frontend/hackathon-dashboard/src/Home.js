import React from 'react';
import './Home.css'; // Import the CSS file
import { Link } from "react-router-dom"; // Import Link

const Home = () => {
    return (
      <div className="home">
        <h1>NAME ENTRY!</h1>
        <p>ENERGY TYPE</p>
        <p>RISK TYPE</p>
  
    {/* Link to Top Performers page */}
    <Link to="/TopPerformers">
        <button>See Top Performers</button>
      </Link>
      </div>
    );
  };
  
  export default Home;
  