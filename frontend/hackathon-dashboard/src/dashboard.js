import React, { useEffect, useState } from "react";
import Papa from "papaparse"; // Import PapaParse
import { Bar } from "react-chartjs-2"; // Import the Bar chart from react-chartjs-2
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";

// Register the necessary components for Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Fetch and parse the CSV file
    Papa.parse("/FSLR_technical 2.csv", {
      download: true,
      header: true, 
      dynamicTyping: true,
      complete: (result) => {
        console.log(result.data); // Check the parsed data
        setData(result.data); 
      },
    });
  }, []); 

  // Prepare data for the bar chart
  const chartData = {
    labels: data.map((row) => new Date(row.Timestamp)), // Convert Timestamp to Date
    
    datasets: [
      {
        label: "Close", // Y-axis data label
        data: data.map((row) => row.close), // Y-axis values (close)
        backgroundColor: "rgba(205, 29, 23, 0.2)", // Bar color
        borderColor: "rgb(218, 20, 20)", // Bar border color
        borderWidth: 1,
      },
    ],
  };

  return (
    <div style={{ width: "50%", margin: "20px auto" }}>
      <h2>Closing Price By Date</h2>

      {/* Render the bar chart */}
      <Bar data={chartData} options={{ responsive: true }} />
    </div>
  );
};

export default Dashboard;
