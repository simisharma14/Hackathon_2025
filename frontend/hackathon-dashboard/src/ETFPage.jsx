import React from "react";
import Layout from "./Layout";
import CombinedChart from "./ETFChart";

const ETFPage = () => {
  return (
    <Layout>
      <div style={{ padding: "20px" }}>
        <h1 style={{ textAlign: "center" }}>ETFs by Sector</h1>
        <p style={{ textAlign: "center" }}>
          Performance comparison of Energy ETFs and SPY benchmark.
        </p>
        <CombinedChart />
      </div>
    </Layout>
  );
};

export default ETFPage;
