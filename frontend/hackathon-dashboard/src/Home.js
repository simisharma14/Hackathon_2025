import "./Home.css";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="home-page-button-container">
      <Link to="/ETFPage">
        <button className="home-page-button">ETF Breakdown</button>
      </Link>

      <Link to="/TopPerformers">
        <button className="home-page-button">Top Performers</button>
      </Link>

      <Link to="/MacroOutlook">
        <button className="home-page-button">Macro Outlook</button>
      </Link>
    </div>
  );
};

export default Home;
