import openai
import os
import yfinance as yf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_stock_data(symbol):
    """
    Fetches basic financial data and market sentiment for the given stock symbol.
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Extract relevant financial data
        stock_data = {
            "Company Name": info.get("longName", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "PE Ratio": info.get("trailingPE", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "52-Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52-Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "Revenue (TTM)": info.get("totalRevenue", "N/A"),
            "EBITDA": info.get("ebitda", "N/A"),
            "Free Cash Flow": info.get("freeCashflow", "N/A"),
            "Net Income": info.get("netIncomeToCommon", "N/A"),
            "Current Price": info.get("currentPrice", "N/A"),
            "Previous Close": info.get("previousClose", "N/A"),
            "Open": info.get("open", "N/A"),
            "Beta": info.get("beta", "N/A"),
            "EPS (TTM)": info.get("trailingEps", "N/A")
        }

        return stock_data

    except Exception as e:
        return {"error": str(e)}


def generate_stock_report(symbol, stock_data):
    """
    Uses OpenAI's GPT to generate a comprehensive stock profile.
    """
    # Convert stock_data dictionary to readable text format
    stock_info_text = "\n".join(
        [f"{key}: {value}" for key, value in stock_data.items()])

    # Define the prompt for the stock profile
    prompt = (
        f"Generate a detailed stock profile for {symbol} based on the following data:\n"
        f"{stock_info_text}\n\n"
        "The report should include:\n"
        "- **Company Overview**: Provide a brief background, industry positioning, and recent performance.\n"
        "- **Strengths & Weaknesses**: Discuss key advantages, risks, and challenges.\n"
        "- **Catalysts for Growth**: Identify upcoming trends, market movements, and potential drivers for future stock price appreciation.\n"
        "- **Market Sentiment Analysis**: Provide insight into current investor sentiment based on financial performance, earnings reports, and recent news.\n"
        "- **Financial Health**: Evaluate the company’s financial stability, debt levels, profitability, and cash flow.\n\n"
        "Ensure the report is professional, insightful, and data-driven. Try to focus on current events in your report, giving actionable items for a potential investor.\nAdditionally, provide information the stocks sector ETF to allow for benchmarking performance against the overall sector. Making sure to include relative valuations in the report."
    )

    # Call the OpenAI API (using the ChatCompletion endpoint)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-3.5-turbo if preferred
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    # Extract the generated content
    outlook = response.choices[0].message["content"]
    return outlook


def main():
    symbol = input(
        "Enter the stock ticker symbol (e.g., AAPL, TSLA, MSFT): ").upper()

    # Fetch stock data
    stock_data = fetch_stock_data(symbol)

    if "error" in stock_data:
        print(f"Error fetching stock data: {stock_data['error']}")
        return

    # Generate stock report using OpenAI
    stock_report = generate_stock_report(symbol, stock_data)

    # Print the report
    print("\n" + "="*50)
    print(f"📊 Stock Profile Report for {symbol}")
    print("="*50)
    print(stock_report)

    # Save the report to a text file
    output_filename = f"./data/ai_reports/{symbol}_stock_profile.txt"
    os.makedirs("./data", exist_ok=True)

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(stock_report)

    print(f"\n✅ Stock profile saved to {output_filename}")


if __name__ == "__main__":
    main()
