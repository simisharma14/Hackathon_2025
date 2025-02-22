import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from 'recharts';

const data = [
  { month: 'Jan', sales: 4000, profit: 2400 },
  { month: 'Feb', sales: 3000, profit: 1398 },
  { month: 'Mar', sales: 5000, profit: 2210 },
  { month: 'Apr', sales: 7000, profit: 2290 },
  { month: 'May', sales: 6000, profit: 2000 },
];

const Dashboard = () => {
  return (
    <div style={{ width: '90%', margin: '20px auto' }}>
      {/* LineChart */}
      <h2>Sales Overview</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="sales" stroke="#8884d8" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>

   
    
    </div>
  );
};

export default Dashboard;
