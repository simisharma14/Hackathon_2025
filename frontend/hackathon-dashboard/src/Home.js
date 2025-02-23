import "./Home.css";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Layout from "./Layout";
import { Link } from "react-router-dom";



const Home = () => {
  const [stockTickers, setStockTickers] = useState([]);
  const [selectedStock, setSelectedStock] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch stock tickers from the API
    axios
      .get("http://127.0.0.1:5000/rankings/10") // This will need to be changed
      .then((response) => {
        console.log("API Response: ", response.data)
        setStockTickers(response.data.rankings);
      })
      .catch((error) => {
        console.error("Error fetching stock tickers:", error);
      });
  }, []);

  // Define the handleStockChange function
  const handleStockChange = (event) => {
    const ticker = event.target.value;
    setSelectedStock(ticker);
    navigate(`/stock/${ticker}`); // Navigate to the stock details page
  };

  return (
    <Layout>
      <Box sx={{ padding: 4, textAlign: "center" }}>
        <Typography variant="h4" gutterBottom>
          Select a Stock
        </Typography>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Select a Stock</InputLabel>
          <Select value={selectedStock} onChange={handleStockChange} displayEmpty>
            {stockTickers.map((stock, index) => (
              <MenuItem key={index} value={stock.ticker}>
                {stock.ticker} - {stock.company_name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

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
      </Box>
    </Layout>
  );
};

export default Home;

