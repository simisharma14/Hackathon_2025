import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

// Example: mapping from ETF ticker to subsector description
function ETFChart({ ticker }) {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // GET from your backend route:
        const response = await fetch(`http://127.0.0.1:5000/csv-data/${ticker}`);
        const data = await response.json();

        if (Array.isArray(data) && !data.error) {
          // Compute percent return relative to first close
          if (data.length > 0) {
            const firstClose = data[0].close;
            const transformed = data.map((item) => {
              const pctReturn = ((item.close - firstClose) / firstClose) * 100;
              return {
                Date: item.timestamp,
                PercentReturn: parseFloat(pctReturn.toFixed(2))
              };
            });
            setChartData(transformed);
          }
        } else {
          console.error(data.error || "No data array returned");
        }
      } catch (err) {
        console.error("Error fetching chart data:", err);
      }
    };

    fetchData();
  }, [ticker]);

  
  return (
    <div
      style={{
        width: "33%", // each chart occupies about one-third of the row
        boxSizing: "border-box",
        padding: "10px"
      }}
    >
      <div
        
      >
        <LineChart
          width={350}
          height={220}
          data={chartData}
          margin={{ top: 20, right: 20, left: 20, bottom: 20 }}
        >
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis dataKey="Date" tickFormatter={() => ""} tickLine={false} axisLine={false} />
          <YAxis
            domain={["auto", "auto"]}
            tickFormatter={(val) => `${val}%`}
          />
          <Tooltip formatter={(val) => `${val}%`} />
          <Line
            type="monotone"
            dataKey="PercentReturn"
            stroke="#09460c"     // <---- green color
            dot={false}
          />
        </LineChart>

  

      </div>
    </div>
  );
}

export default ETFChart;
