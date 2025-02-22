from flask import Flask, jsonify
import pandas as pd
import os

# Import scripts
from sentiment_analysis import add_finbert_sentiment
from company_profile_builder import pull_advanced_metrics
from ranking_algorithm import build_stocks_metrics, rank_stocks

app = Flask(__name__)

DATA_PATH = "./data"


@app.route("/")
def home():
    return jsonify({"message": "Stock Sentiment & Financial API is Running!"})

# ==========================
# 1) Fetch Sentiment Analysis
# ==========================


@app.route("/sentiment/<symbol>", methods=["GET"])
def get_sentiment(symbol):
    try:
        file_path = f"{DATA_PATH}/sentiment_scores/{symbol}_sentiment_news.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Sentiment data not found for stock"}), 404

        df_sentiment = pd.read_csv(file_path)
        sentiment_data = df_sentiment.to_dict(orient="records")

        return jsonify({"symbol": symbol, "sentiment_data": sentiment_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# 2) Fetch Stock Financial Metrics
# ==========================


@app.route("/financials/<symbol>", methods=["GET"])
def get_financials(symbol):
    try:
        file_path = f"./advanced_metrics/{symbol}_advanced_metrics.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Financial data not found"}), 404

        df_financials = pd.read_csv(file_path)
        financial_data = df_financials.to_dict(orient="records")[0]

        return jsonify({"symbol": symbol, "financial_data": financial_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# 3) Fetch Ranked Stocks
# ==========================


@app.route("/rankings", methods=["GET"])
def get_rankings():
    try:
        SYMBOLS = ["NEE", "FSLR", "ENPH", "RUN", "SEDG", "CSIQ", "JKS"]
        df_stocks = pd.DataFrame(columns=[
            'ticker', 'sentiment_score', 'ebitda', 'five_yr_rev_cagr', 'ev_ebitda', 'roic', 'fcf_yield'])

        # Aggregate sentiment & financial data
        for symbol in SYMBOLS:
            df_stocks = build_stocks_metrics(symbol, df_stocks)

        # Rank stocks
        df_ranked = rank_stocks(df_stocks)

        # Convert to JSON
        ranked_data = df_ranked.to_dict(orient="records")
        return jsonify({"rankings": ranked_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
