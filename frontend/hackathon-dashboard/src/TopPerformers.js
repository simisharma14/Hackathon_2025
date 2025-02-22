import React, { useEffect, useState } from "react";
import axios from "axios";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import Layout from "./Layout";

const TopPerformers = () => {
  const [topStocks, setTopStocks] = useState([]);

  useEffect(() => {
    // Fetch top 10 ranked stocks from API
    axios
      .get("http://127.0.0.1:5000/rankings/10")
      .then((response) => {
        setTopStocks(response.data.rankings);
      })
      .catch((error) => {
        console.error("Error fetching ranked stocks:", error);
      });
  }, []);

  return (
    <Layout>
      <Box sx={{ padding: 4 }}>
        <Typography variant="h4" gutterBottom>
          Top Performers
        </Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          Here are the top 10 ranked energy stocks based on our ranking
          algorithm.
        </Typography>
        <Grid container spacing={3}>
          {topStocks.map((stock, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card
                variant="outlined"
                sx={{
                  minWidth: 275,
                  border: "2px solid #09460c",
                  borderRadius: "8px",
                  boxShadow: "3px 3px 10px rgba(0, 0, 0, 0.1)",
                }}
              >
                <CardContent>
                  <Typography
                    sx={{ fontSize: 14, color: "text.secondary" }}
                    gutterBottom
                  >
                    Rank #{stock.rank}
                  </Typography>
                  <Typography variant="h5" component="div">
                    {stock.ticker}
                  </Typography>
                  <Typography sx={{ mb: 1.5 }} color="text.secondary">
                    {stock.company_name}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Sentiment Score:</strong>{" "}
                    {stock.sentiment_score.toFixed(2)}
                    <br />
                    <strong>Implied Upside:</strong>{" "}
                    {stock.implied_upside.toFixed(2)}%
                    <br />
                    <strong>Volatility:</strong> {stock.volatility.toFixed(2)}%
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    href={`/stock/${stock.ticker}`}
                    variant="contained"
                    sx={{
                      backgroundColor: "#09460c",
                      color: "#fff",
                      "&:hover": {
                        backgroundColor: "#063307",
                      },
                    }}
                  >
                    View Details
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Layout>
  );
};

export default TopPerformers;
