
import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

// ETFs (including SPY) and their subsectors:
const ETF_SUBSECTORS = {
  NLR: "Nuclear",
  TAN: "Solar",
  FAN: "Wind",
  ICLN: "Clean Energy",
  PBW: "Clean Energy",
  HYDR: "Hydrogen",
  SPY: "Benchmark",
};

// Tickers we'll plot
const etfTickers = Object.keys(ETF_SUBSECTORS);

// Define colors for each ticker
const tickerColors = {
  NLR: "#4287f5",  // blue
  TAN: "#f54242",  // red
  FAN: "#42f554",  // green
  ICLN: "#f5a142", // orange
  PBW: "#42f5e0",  // cyan
  HYDR: "#a142f5", // purple
  SPY: "#000000",  // black
};

const CombinedChart = () => {
  const [combinedData, setCombinedData] = useState([]);

  useEffect(() => {
    // Fetch data for each ticker
    const fetchTickerData = async (ticker) => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/csv-data/${ticker}`);
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          const firstClose = data[0].close;
          return data.map((item) => ({
            Date: item.timestamp, // e.g. "YYYY-MM-DD HH:mm:ss"
            [ticker]: ((item.close - firstClose) / firstClose) * 100, // % return
          }));
        } else {
          console.error(`No array returned for ${ticker}`, data);
          return [];
        }
      } catch (err) {
        console.error(`Error fetching data for ${ticker}:`, err);
        return [];
      }
    };

    // Fetch all tickers concurrently
    Promise.all(etfTickers.map((ticker) => fetchTickerData(ticker))).then(
      (allDataArrays) => {
        // Merge them into one combined array keyed by Date.
        const combinedMap = {};
        allDataArrays.forEach((dataArray) => {
          dataArray.forEach((record) => {
            const date = record.Date;
            if (!combinedMap[date]) {
              combinedMap[date] = { Date: date };
            }
            Object.keys(record).forEach((key) => {
              if (key !== "Date") {
                // round to 2 decimals
                combinedMap[date][key] = parseFloat(record[key].toFixed(2));
              }
            });
          });
        });

        // Convert combinedMap to sorted array by date
        const merged = Object.values(combinedMap).sort(
          (a, b) => new Date(a.Date) - new Date(b.Date)
        );
        setCombinedData(merged);
      }
    );
  }, []);

  return (
    <div
      style={{
        margin: "0 auto",
        textAlign: "center",
        padding: "20px",
        maxWidth: "1200px",
      }}
    >
      <LineChart
        width={1000}    // Increase width
        height={500}    // Increase height
        data={combinedData}
        margin={{ top: 20, right: 40, left: 20, bottom: 20 }}
        style={{ margin: "0 auto" }} // further ensure centering
      >
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        {/* Hide X-axis ticks (optional) */}
        <XAxis dataKey="Date" tick={false} axisLine={false} />
        <YAxis tickFormatter={(val) => `${val.toFixed(1)}%`} />
        <Tooltip formatter={(val) => `${val.toFixed(2)}%`} />
        <Legend />
        {etfTickers.map((ticker) => (
          <Line
            key={ticker}
            type="monotone"
            dataKey={ticker}
            // name includes subsector
            name={`${ticker} (${ETF_SUBSECTORS[ticker]})`}
            stroke={tickerColors[ticker] || "#000000"}
            dot={false}
          />
        ))}
      </LineChart>
    </div>
  );
};

export default CombinedChart;
