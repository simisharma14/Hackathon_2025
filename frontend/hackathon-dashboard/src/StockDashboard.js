/*
// pages/StockDashboard.js
import { useState, useEffect } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent } from "@/components/ui/card";

//Only added from ARL to IDA
//const stockOptions = ["ARL", "ARRY", "BEP", "BE", "BLDP", "BWXT", "BW", "CCJ", "CEG", "CSIG", "CWEN", "DNNGY", "DQ", "ENPH", "EVA", "FSLR", "GE", "GPRE", "IBDRY", "IDA"];
const stockOptions = ["CSIQ", "ENPH", "FSLR", "JKS", "NEE", "NXT", "RUN", "SEDG"]

export default function StockDashboard() {
    const [selectedStock, setSelectedStock] = useState(null);
    const [stockData, setStockData] = useState([]);
  
    useEffect(() => {
      const fetchStockData = async () => {
        if (!selectedStock) return; // If no stock is selected, do nothing
  
        try {
          const response = await axios.get(`https://finnhub.io/api/v1/stock/candle`, {
            params: {
              symbol: selectedStock,
              resolution: "D",
              from: Math.floor(Date.now() / 1000) - 604800, // last 7 days
              to: Math.floor(Date.now() / 1000),
              token: "YOUR_API_KEY", // Replace with your actual API key
            },
          });
  
          const formattedData = response.data.t.map((time, index) => ({
            date: new Date(time * 1000).toLocaleDateString(),
            price: response.data.c[index],
          }));
  
          setStockData(formattedData);
        } catch (error) {
          console.error(`Error fetching data for ${selectedStock}:`, error);
        }
      };
  
      fetchStockData();
    }, [selectedStock]);
  
    return (
      <div className="p-8">
        <h1 className="text-3xl font-bold mb-4">Stock Dashboard</h1>
  
        {/* Radio Button Selection }
        <div className="mb-4">
          <h2 className="text-xl font-semibold mb-2">Select a Stock:</h2>
          {stockOptions.map((stock) => (
            <div key={stock} className="flex items-center mb-2">
              <input
                type="radio"
                name="stock"
                value={stock}
                checked={selectedStock === stock}
                onChange={() => setSelectedStock(stock)}
                className="w-5 h-5 accent-blue-500 cursor-pointer"
              />
              <label className="ml-2">{stock}</label>
            </div>
          ))}
        </div>
  
        {/* Stock Chart }
        {selectedStock && (
          <Card>
            <CardContent>
              <h2 className="text-lg font-semibold">{selectedStock} Stock Price</h2>
              <LineChart
                width={600}
                height={300}
                data={stockData}
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="price" stroke="#8884d8" />
              </LineChart>
            </CardContent>
          </Card>
        )}
      </div>
    );
  }
*/