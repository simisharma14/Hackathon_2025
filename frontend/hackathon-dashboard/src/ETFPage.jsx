import React from "react";
import Layout from "./Layout";
import ETFChart from "./ETFChart";

const ETFPage = () => {
  const etfTickers = ["NLR", "TAN", "FAN", "ICLN", "PBW", "HYDR"];

  // Mapping each ticker to its subsector
  const ETF_SUBSECTORS = {
    NLR: "Nuclear",
    TAN: "Solar",
    FAN: "Wind",
    ICLN: "Clean Energy",
    PBW: "Clean Energy",
    HYDR: "Hydrogen"
  };

  return (
    <Layout>
      <div style={{ padding: "20px" }}>
        <h1 style={{ textAlign: "center" }}>ETFs by Sector</h1>
        <p style={{ textAlign: "center" }}>Here's a breakdown of ETFs by energy type.</p>
        
        {/* Container for all charts */}
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",          // allow wrapping
            justifyContent: "space-between",
            gap: "20px",               // space between items
            maxWidth: "1200px",        // optional: limit container width
            margin: "0 auto"           // center container
          }}
        >
          {etfTickers.map((ticker) => (
            <div
              key={ticker}
              style={{
                flex: "1 1 calc(33.333% - 20px)", // about one-third width
                minWidth: "250px",               // prevent items from shrinking too small
                boxSizing: "border-box",
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "10px",
                background: "#fff"
              }}
            >
              {/* Chart component */}
              <ETFChart ticker={ticker} />

              {/* Ticker + Subsector label */}
              <div style={{ textAlign: "center", marginTop: "10px", fontWeight: "bold" }}>
                {ticker}{" "}
                {ETF_SUBSECTORS[ticker] && (
                  <span style={{ fontWeight: "normal", marginLeft: "4px" }}>
                    ({ETF_SUBSECTORS[ticker]})
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
};

export default ETFPage;
