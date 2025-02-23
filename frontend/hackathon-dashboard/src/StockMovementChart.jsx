import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  // Legend is omitted on purpose
} from "recharts";
import { Box, Button, ButtonGroup, CircularProgress, Typography } from "@mui/material";

const StockMovementChart = ({ symbol }) => {
  const [fullData, setFullData] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [period, setPeriod] = useState("all");
  const [loading, setLoading] = useState(true);

  // Fetch full historical data from the backend route
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/stock-price/all/${symbol}`);
        const data = await response.json();
        setFullData(data);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching full historical data:", err);
        setLoading(false);
      }
    };
    fetchData();
  }, [symbol]);

  // Filter data based on selected period
  useEffect(() => {
    if (!fullData || fullData.length === 0) return;
    const now = new Date();
    let filteredData = [];
    if (period === "day") {
      // Use the last date in fullData to filter
      const latestDate = new Date(fullData[fullData.length - 1].timestamp);
      filteredData = fullData.filter((record) => {
        const recDate = new Date(record.timestamp);
        return recDate.toDateString() === latestDate.toDateString();
      });
    } else if (period === "week") {
      const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
      filteredData = fullData.filter((record) => new Date(record.timestamp) >= weekAgo);
    } else if (period === "year") {
      const yearAgo = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
      filteredData = fullData.filter((record) => new Date(record.timestamp) >= yearAgo);
    } else {
      // all time
      filteredData = fullData;
    }
    // Sort by date ascending
    const sorted = filteredData.sort(
      (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
    );
    setChartData(sorted);
  }, [fullData, period]);

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: 300 }}>
        <CircularProgress />
      </Box>
    );
  }

  // A small helper function to style the buttons
  const getButtonStyle = (buttonPeriod) => {
    const isActive = period === buttonPeriod;
    return {
      backgroundColor: isActive ? "#09460c" : "#e0e0e0",
      color: isActive ? "#ffffff" : "#333",
      border: isActive ? "1px solid #09460c" : "1px solid #ccc",
      transition: "background-color 0.3s ease",
      // Optional hover style:
      "&:hover": {
        backgroundColor: isActive ? "#09460c" : "#d5d5d5",
      },
    };
  };

  return (
    <Box sx={{ textAlign: "center", marginBottom: 4 }}>
      <Typography variant="h5" gutterBottom>
        Stock Movement
      </Typography>
      <ButtonGroup sx={{ marginBottom: 2 }}>
        <Button sx={getButtonStyle("day")} onClick={() => setPeriod("day")}>
          Day
        </Button>
        <Button sx={getButtonStyle("week")} onClick={() => setPeriod("week")}>
          Week
        </Button>
        <Button sx={getButtonStyle("year")} onClick={() => setPeriod("year")}>
          Year
        </Button>
        <Button sx={getButtonStyle("all")} onClick={() => setPeriod("all")}>
          All Time
        </Button>
      </ButtonGroup>

      <Box sx={{ overflowX: "auto", margin: "0 auto" }}>
        <LineChart
          width={1000}
          height={500}
          data={chartData}
          margin={{ top: 20, right: 40, left: 20, bottom: 20 }}
          style={{ margin: "0 auto" }}
        >
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(value) =>
              new Date(value).toLocaleDateString(undefined, { month: "short", day: "numeric" })
            }
          />
          <YAxis tickFormatter={(val) => `$${val}`} />
          <Tooltip
            labelFormatter={(label) =>
              new Date(label).toLocaleDateString() + " " + new Date(label).toLocaleTimeString()
            }
            formatter={(val) => `$${val}`}
          />
          {/* We omit <Legend /> so there's no legend */}
          <Line type="monotone" dataKey="close" stroke="#f54242" dot={false} />
        </LineChart>
      </Box>
    </Box>
  );
};

export default StockMovementChart;
