import React, { useState, useEffect } from "react";
import axios from "axios";
import Layout from "./Layout";
import {
  Box,
  Typography,
  CircularProgress,
  Card,
  CardContent,
} from "@mui/material";
import { useGlobalContext } from "./GlobalContext";

const InvestmentStrategyPage = () => {
  const [strategy, setStrategy] = useState("");
  const [loading, setLoading] = useState(false);
  const { userData } = useGlobalContext();

  useEffect(() => {
    setLoading(true);
    axios
      .get(
        `http://127.0.0.1:5000/investment-strategy/${userData.riskTolerance.toLowerCase()}`
      )
      .then((response) => {
        setStrategy(response.data.investment_strategy);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching investment strategy:", error);
        setLoading(false);
      });
  }, [userData.riskTolerance, userData.energyType]);

  return (
    <Layout>
      <Box sx={{ padding: 4, textAlign: "center" }}>
        <Typography variant="h4" gutterBottom>
          Personalized Investment Strategy
        </Typography>

        {loading ? (
          <Box sx={{ display: "flex", justifyContent: "center", marginTop: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Card
            variant="outlined"
            sx={{ marginTop: 3, padding: 3, textAlign: "left" }}
          >
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Investment Strategy for {userData.energyType} Sector
              </Typography>
              <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                {strategy}
              </Typography>
            </CardContent>
          </Card>
        )}
      </Box>
    </Layout>
  );
};

export default InvestmentStrategyPage;
