import yfinance as yf
from flask import Flask, jsonify, Response
import pandas as pd
import os
import openai
from flask_cors import CORS

# Import scripts
from sentiment_analysis import add_finbert_sentiment
from company_profile_builder import pull_advanced_metrics
from ranking_algorithm import build_stocks_metrics, rank_stocks
from stock_AI_prompt import fetch_stock_data, generate_stock_report
from flask_cors import CORS
from investment_strategy import generate_investment_strategy

app = Flask(__name__)
CORS(app)

DATA_PATH = "./data"


@app.route("/")
def home():
    return jsonify({"message": "Stock Sentiment & Financial API is Running!"})


# Load stock rankings
df_ranked = pd.read_csv("./stocks_ranked.csv")


@app.route("/investment-strategy/<risk_tolerance>", methods=["GET"])
def get_investment_strategy(risk_tolerance):
    """
    API endpoint to generate a personalized investment strategy.
    Requires query parameters: risk_tolerance and sector_preference.
    """
    risk_tolerance = risk_tolerance.capitalize()
    sector_preference = sector_preference.capitalize()

    strategy = generate_investment_strategy(
        risk_tolerance, df_ranked)

    return jsonify({
        "risk_tolerance": risk_tolerance,
        "sector_preference": sector_preference,
        "investment_strategy": strategy
    })


@app.route("/csv-data/<symbol>", methods=["GET"])
def get_csv_data(symbol):
    csv_file = os.path.join("./company_profiles",
                            f"{symbol}_technical_all_time.csv")
    if not os.path.exists(csv_file):
        return jsonify({"error": "CSV file not found"}), 404

    try:
        df = pd.read_csv(csv_file)
        # Replace NaN with None so that they become null in JSON
        df = df.where(pd.notnull(df), None)
        json_str = df.to_json(orient="records")
        return Response(json_str, mimetype="application/json")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ==========================
# 1) Fetch Sentiment Analysis
# ==========================


def generate_macro_outlook():
    prompt = (
        "Write a comprehensive macro outlook report for the energy sector. "
        "Include discussions of renewable energy, nuclear, solar, wind, hydropower, and geothermal trends, "
        "as well as recent regulatory changes and government policies. "
        "Highlight key market trends, international developments, and potential future challenges and opportunities. "
        "Conclude with a summary and key takeaways."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )

    outlook = response.choices[0].message["content"]
    return outlook


@app.route("/macro-outlook", methods=["GET"])
def get_macro_outlook():
    outlook_report = generate_macro_outlook()
    return jsonify({"outlook_report": outlook_report})


@app.route("/sentiment/stock/<symbol>", methods=["GET"])
def get_sentiment_stock(symbol):
    try:
        file_path = f"{DATA_PATH}/sentiment_scores/stocks/{symbol}_sentiment_news.csv"
        if not os.path.exists(file_path):
            return jsonify({"error": "Sentiment data not found for stock"}), 404

        df_sentiment = pd.read_csv(file_path)
        sentiment_data = df_sentiment.to_dict(orient="records")

        return jsonify({"symbol": symbol, "sentiment_data": sentiment_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sentiment/ETF/<symbol>", methods=["GET"])
def get_sentiment_etf(symbol):
    try:
        file_path = f"{DATA_PATH}/sentiment_scores/ETFs/{symbol}_sentiment_news.csv"
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
        SYMBOLS = ["NEE", "FSLR", "ENPH", "RUN", "SEDG",
                   "CSIQ", "JKS", "NXT", "DQ", "ARRY", "GE", "VWS", "IBDRY", "DNNGY", 'BEP', "NPI", "CWEN", "INOXWIND", "ORA", "IDA", "OPTT", "DRXGY", "EVA", "GPRE", "PLUG", "BE", "BLDP", "ARL", "OPTT", "CEG", "VST", "CCJ", "LEU", "SMR", "OKLO", "NNE", "BWXT", "BW"
                   ]
        df_stocks = pd.DataFrame(columns=[
            'ticker', 'sentiment_score', 'ebitda', 'five_yr_rev_cagr', 'ev_ebitda', 'roic', 'fcf_yield', 'volatility', 'implied_upside', 'sharpe_ratio'])

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


@app.route("/rankings/<int:n>", methods=["GET"])
def get_top_n_rankings(n):
    try:
        SYMBOLS = ["NEE", "FSLR", "ENPH", "RUN", "SEDG",
                   "CSIQ", "JKS", "NXT", "DQ", "ARRY", "GE", "VWS", "IBDRY", "DNNGY", 'BEP', "NPI", "CWEN", "INOXWIND", "ORA", "IDA", "OPTT", "DRXGY", "EVA", "GPRE", "PLUG", "BE", "BLDP", "ARL", "OPTT", "CEG", "VST", "CCJ", "LEU", "SMR", "OKLO", "NNE", "BWXT", "BW"
                   ]
        df_stocks = pd.DataFrame(columns=[
            'ticker', 'sentiment_score', 'ebitda', 'five_yr_rev_cagr', 'ev_ebitda', 'roic', 'fcf_yield', 'volatility', 'implied_upside', 'sharpe_ratio'])

        # Aggregate sentiment & financial data
        for symbol in SYMBOLS:
            df_stocks = build_stocks_metrics(symbol, df_stocks)

        # Rank stocks
        df_ranked = rank_stocks(df_stocks)
        df_ranked = df_ranked[df_ranked['rank'] <= n]

        # Convert to JSON
        ranked_data = df_ranked.to_dict(orient="records")
        return jsonify({"rankings": ranked_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================
# 1) Get Top Performers
# ==========================
@app.route("/top-performers", methods=["GET"])
def get_top_performers():
    """
    Fetches the top-rated stocks based on ranking algorithm and provides key metrics.
    """
    try:
        # Load rankings
        ranking_file = "./stocks_ranked.csv"
        if not os.path.exists(ranking_file):
            return jsonify({"error": "Ranked stock data not found"}), 404

        df_ranked = pd.read_csv(ranking_file)

        # Select top 10 performers
        df_top = df_ranked.head(
            10)[["ticker", "sentiment_score", "implied_upside"]]

        # Convert to JSON
        top_data = df_top.to_dict(orient="records")
        return jsonify({"top_performers": top_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stock-price/all/<symbol>", methods=["GET"])
def get_stock_price_all(symbol: str):
    try:
        df = pd.read_csv(
            f"./company_profiles/{symbol.upper()}_technical_all_time.csv")
        return df[["timestamp", "close"]].to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.route("/stock-price/<symbol>/<start_date>/<end_date>", methods=["GET"])
def get_stock_price_data(symbol: str, start_date: str, end_date: str):
    """
    Fetches historical stock price data between start_date and end_date.

    Args:
        symbol (str): Stock ticker (e.g., "AAPL").
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        list: List of {"Date": date, "Close": closing_price}.
    """
    try:
        stock = yf.Ticker(symbol)
        df_history = stock.history(start=start_date, end=end_date, period="1d")

        if df_history.empty:
            return {"error": f"No stock price data available for {symbol} between {start_date} and {end_date}"}

        # Format data
        df_history.reset_index(inplace=True)
        df_history["Date"] = df_history["Date"].dt.strftime("%Y-%m-%d")

        return df_history[["Date", "Close"]].to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


@app.route("/financial-statements/<symbol>", methods=["GET"])
def fetch_financial_statements(symbol: str):
    """
    Fetches balance sheet, income statement, and cash flow statement for a given stock symbol.
    """
    try:
        stock = yf.Ticker(symbol)
        financials = {
            "Balance Sheet": stock.balance_sheet.to_dict(),
            "Income Statement": stock.financials.to_dict(),
            "Cash Flow Statement": stock.cashflow.to_dict()
        }
        return financials
    except Exception as e:
        return {"error": str(e)}


@app.route("/stock-profile/<symbol>", methods=["GET"])
def get_stock_profile(symbol: str):
    """
    API endpoint to generate a stock profile report.
    """
    symbol = symbol.upper()
    stock_data = fetch_stock_data(symbol)

    if "error" in stock_data:
        return jsonify({"error": stock_data["error"]}), 500

    stock_report = generate_stock_report(symbol, stock_data)

    # Save the AI-generated report to a text file
    output_filename = f"./data/ai_reports/{symbol}_stock_profile.txt"
    os.makedirs("./data/ai_reports", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(stock_report)

    return jsonify({
        "symbol": symbol,
        "stock_data": stock_data,
        "stock_report": stock_report,
        "report_saved": output_filename
    })


if __name__ == "__main__":
    app.run(debug=True)
