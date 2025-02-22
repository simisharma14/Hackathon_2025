import React, { useEffect, useState } from "react";
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

const MacroOutlook = () => {
  const [outlookReport, setOutlookReport] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [hasFetched, setHasFetched] = useState(false); // Prevent duplicate fetch

  useEffect(() => {
    if (!hasFetched) {
      setHasFetched(true); // Mark as fetched to avoid re-fetching

      axios
        .get("http://127.0.0.1:5000/macro-outlook")
        .then((response) => {
          setOutlookReport(response.data.outlook_report);
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error fetching macro outlook report:", error);
          setError("Failed to load macro outlook report. Please try again.");
          setLoading(false);
        });
    }
  }, [hasFetched]); // Dependency array ensures it runs only once

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
          Macro Outlook for the Energy Sector
        </Typography>

        <Card
          variant="outlined"
          sx={{
            padding: 2,
            border: "2px solid #09460c",
            backgroundColor: "#f9f9f9",
          }}
        >
          <CardContent>
            <ReactMarkdown>{outlookReport}</ReactMarkdown>
          </CardContent>
        </Card>
      </Box>
    </Layout>
  );
};

export default MacroOutlook;
