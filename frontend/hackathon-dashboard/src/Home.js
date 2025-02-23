import "./Home.css";
import { Link } from "react-router-dom";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Layout from "./Layout";



const Home = () => {
    const stockTickers = [
        "NEE", "FSLR", "ENPH", "RUN", "SEDG",
        "CSIQ", "JKS", "NXT", "DQ", "ARRY", "GE", "VWS", "IBDRY", "DNNGY",
        "BEP", "NPI", "CWEN", "INOXWIND", "ORA", "IDA", "OPTT", "DRXGY", "EVA",
        "GPRE", "PLUG", "BE", "BLDP", "ARL", "CEG", "VST", "CCJ", "LEU", "SMR",
        "OKLO", "NNE", "BWXT", "BW"
      ];
      
      const [selectedStock, setSelectedStock] = useState("");
      const navigate = useNavigate();
      
      const handleStockChange = (event) => {
        const ticker = event.target.value;
        setSelectedStock(ticker);
        navigate(`/stock/${ticker}`); // Navigate to the stock details page
      };
      
      return (
        <Layout>
          <Box sx={{ padding: 10, textAlign: "center" }}>
          <Typography variant="h3" className="home-title">
          View Clean Energy Stock Performance, Analyses, and AI-Recommendations
        </Typography>
        <Box className="home-container">
            <Typography variant="h4" gutterBottom>
              Select a Stock
            </Typography>
            <FormControl sx={{ minWidth: 200 }}>
              <InputLabel>Select a Stock</InputLabel>
              <Select value={selectedStock} onChange={handleStockChange} displayEmpty>
                {stockTickers.map((ticker, index) => (
                  <MenuItem key={index} value={ticker}>
                    {ticker}
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
      </Box>
    </Layout>

  );
};

export default Home;

