import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import Layout from "./Layout";
import {
  Box,
  Typography,
  CircularProgress,
  Card,
  CardContent,
} from "@mui/material";

const StockProfile = () => {
  const { symbol } = useParams();
  const [formattedMarkdown, setFormattedMarkdown] = useState("");
  const [stockData, setStockData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/stock-profile/${symbol}`)
      .then((response) => {
        setFormattedMarkdown(formatMarkdown(response.data.stock_report));
        setStockData(response.data.stock_data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching stock profile:", error);
        setError("Failed to load stock data. Please try again.");
        setLoading(false);
      });
  }, [symbol]);

  // Function to convert raw text to Markdown format
  const formatMarkdown = (rawText) => {
    return rawText
      .split("**") // Split at bold markers
      .map((section, index) =>
        index % 2 === 1 ? `### ${section.trim()}` : section.trim()
      )
      .join("\n\n");
  };

  if (loading) {
    return (
      <Layout>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "80vh",
          }}
        >
          <CircularProgress />
        </Box>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout>
        <Box sx={{ textAlign: "center", padding: 4 }}>
          <Typography variant="h5" color="error">
            {error}
          </Typography>
        </Box>
      </Layout>
    );
  }

  return (
    <Layout>
      <Box sx={{ padding: 4 }}>
        <Typography variant="h4" gutterBottom>
          {stockData["Company Name"]} ({symbol.toUpperCase()})
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          {stockData["Sector"]} - {stockData["Industry"]}
        </Typography>

        {/* Stock Overview Section */}
        <Card
          variant="outlined"
          sx={{
            marginY: 3,
            padding: 2,
            border: "2px solid #09460c", // Dark green border
            backgroundColor: "#f9f9f9",
          }}
        >
          <CardContent>
            <Typography variant="body1" sx={{ marginTop: 1 }}>
              {formattedMarkdown ? (
                <ReactMarkdown>{formattedMarkdown}</ReactMarkdown>
              ) : (
                "No AI-generated report available."
              )}
            </Typography>
          </CardContent>
        </Card>

        {/* Stock Data Section */}
        <Card
          variant="outlined"
          sx={{
            padding: 2,
            border: "2px solid #09460c", // Matching dark green border
            backgroundColor: "#f9f9f9",
          }}
        >
          <CardContent>
            <Typography variant="h5">Financial Data</Typography>
            <Typography variant="body1">
              <strong>Market Cap:</strong> $
              {stockData["Market Cap"]?.toLocaleString()}
            </Typography>
            <Typography variant="body1">
              <strong>PE Ratio:</strong> {stockData["PE Ratio"]}
            </Typography>
            <Typography variant="body1">
              <strong>EBITDA:</strong> ${stockData["EBITDA"]?.toLocaleString()}
            </Typography>
            <Typography variant="body1">
              <strong>Free Cash Flow:</strong> $
              {stockData["Free Cash Flow"]?.toLocaleString()}
            </Typography>
            <Typography variant="body1">
              <strong>Net Income:</strong> $
              {stockData["Net Income"]?.toLocaleString()}
            </Typography>
            <Typography variant="body1">
              <strong>52-Week High:</strong> ${stockData["52-Week High"]}
            </Typography>
            <Typography variant="body1">
              <strong>52-Week Low:</strong> ${stockData["52-Week Low"]}
            </Typography>
            <Typography variant="body1">
              <strong>Dividend Yield:</strong> {stockData["Dividend Yield"]}%
            </Typography>
            <Typography variant="body1">
              <strong>Beta:</strong> {stockData["Beta"]}
            </Typography>
            <Typography variant="body1">
              <strong>Current Price:</strong> ${stockData["Current Price"]}
            </Typography>
            <Typography variant="body1">
              <strong>Previous Close:</strong> ${stockData["Previous Close"]}
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Layout>
  );
};

export default StockProfile;
