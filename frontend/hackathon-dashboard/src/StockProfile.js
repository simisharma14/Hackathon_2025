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
import StockMovementChart from "./StockMovementChart"; // your custom chart component

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
      .catch((err) => {
        console.error("Error fetching stock profile:", err);
        setError("Failed to load stock data. Please try again.");
        setLoading(false);
      });
  }, [symbol]);

  // Convert raw text (with **bold** markers) to simpler Markdown
  const formatMarkdown = (rawText) => {
    return rawText
      .split("**")
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
        {/* Company Name & Symbol */}
        <Typography variant="h4" gutterBottom>
          {stockData["Company Name"]} ({symbol.toUpperCase()})
        </Typography>

        {/* CHART SECTION */}
        <StockMovementChart symbol={symbol} />

        {/* Financial Overview Section */}
        <Card
          variant="outlined"
          sx={{
            padding: 2,
            border: "2px solid #09460c",
            backgroundColor: "#f9f9f9",
            marginBottom: 3,
            marginTop: 3,
          }}
        >
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Financial Overview
            </Typography>
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", md: "repeat(3, 1fr)" },
                gap: 2,
                marginTop: 2,
                textAlign: "left",
              }}
            >
              {/* Column 1 */}
              <Box>
                <Typography variant="body1">
                  <strong>Previous Close:</strong>{" "}
                  ${stockData["Previous Close"] || "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>Open:</strong> ${stockData["Open"] || "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>52-Week High:</strong>{" "}
                  ${stockData["52-Week High"] || "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>52-Week Low:</strong>{" "}
                  ${stockData["52-Week Low"] || "N/A"}
                </Typography>
              </Box>
              {/* Column 2 */}
              <Box>
                <Typography variant="body1">
                  <strong>Market Cap:</strong>{" "}
                  {stockData["Market Cap"]
                    ? `$${stockData["Market Cap"].toLocaleString()}`
                    : "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>Beta:</strong> {stockData["Beta"] || "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>PE Ratio:</strong> {stockData["PE Ratio"] || "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>Dividend Yield:</strong>{" "}
                  {stockData["Dividend Yield"]
                    ? `${stockData["Dividend Yield"]}%`
                    : "N/A"}
                </Typography>
              </Box>
              {/* Column 3 */}
              <Box>
                <Typography variant="body1">
                  <strong>Current Price:</strong>{" "}
                  ${stockData["Current Price"] || "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>EBITDA:</strong>{" "}
                  {stockData["EBITDA"]
                    ? `$${stockData["EBITDA"].toLocaleString()}`
                    : "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>Free Cash Flow:</strong>{" "}
                  {stockData["Free Cash Flow"]
                    ? `$${stockData["Free Cash Flow"].toLocaleString()}`
                    : "N/A"}
                </Typography>
                <Typography variant="body1">
                  <strong>Net Income:</strong>{" "}
                  {stockData["Net Income"]
                    ? `$${stockData["Net Income"].toLocaleString()}`
                    : "N/A"}
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        {/* AI-generated Report Section */}
        <Card
          variant="outlined"
          sx={{
            marginY: 3,
            padding: 2,
            border: "2px solid #09460c",
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
      </Box>
    </Layout>
  );
};

export default StockProfile;
