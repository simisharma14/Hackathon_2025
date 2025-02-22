import React from "react";
import Layout from "./Layout"; // Import Layout

const ETFPage = () => {
  return (
    <Layout>
      <div className="etf">
        <h1>ETFs by Sector</h1>
        <p>Here's a break down of ETFs by energy type.</p>
      </div>
    </Layout>
  );
};

export default ETFPage;