import React, { useEffect, useState } from "react";
import Papa from "papaparse"; // Import PapaParse

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

  return (
    <div style={{ width: "90%", margin: "20px auto" }}>
      <h2>CSV Data</h2>

      {/* Display data as a table */}
      <table border="1" style={{ width: "100%", marginTop: "20px" }}>
        <thead>
          <tr>
            {data.length > 0 && Object.keys(data[0]).map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, idx) => (
                <td key={idx}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
