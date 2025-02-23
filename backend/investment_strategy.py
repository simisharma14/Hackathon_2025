import openai
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_investment_strategy(risk_tolerance, top_stocks):
    """
    Generates a tailored investment strategy based on risk tolerance, sector preference, and top-rated stocks.

    Args:
        risk_tolerance (str): "Low", "Medium", or "High"
        top_stocks (pd.DataFrame): DataFrame of ranked stocks

    Returns:
        str: AI-generated investment strategy
    """

    # Select top 5 based on ranking
    recommended_stocks = top_stocks.head(
        5) if not top_stocks.empty else top_stocks.head(5)

    # Convert recommended stocks to a text list
    stock_list = "\n".join(
        [f"- {row['ticker']} - Sharpe Ratio: {row['sharpe_ratio']:.2f}"
         for _, row in recommended_stocks.iterrows()]
    )

    # Define the AI prompt
    prompt = (
        f"Create a personalized investment strategy for an investor with {risk_tolerance.lower()} risk tolerance, "
        f"Here are the top-rated stocks based on our financial ranking system:\n\n{stock_list}\n\n"
        "The strategy should include:\n"
        "- An overview of the sector and why it's a strong investment choice.\n"
        "- Portfolio allocation recommendations (e.g., % allocation to each stock).\n"
        "- Risk mitigation strategies based on risk tolerance.\n"
        "- Key market trends, financial metrics, and potential catalysts for growth.\n"
        "- Diversification suggestions and alternative energy sectors to consider.\n"
        "The investment strategy should be professional, insightful, and data-driven."
    )

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use GPT-4 for better insights
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    # Extract and return the response
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # Example Usage
    df_ranked = pd.read_csv("./stocks_ranked.csv")  # Load ranked stocks
    user_risk_tolerance = "Low"  # Low, Medium, High

    strategy = generate_investment_strategy(
        user_risk_tolerance, df_ranked)

    print("\n=== Personalized Investment Strategy ===\n")
    print(strategy)

    # Save to file
    os.makedirs("./data/investment_strategies", exist_ok=True)
    filename = f"./data/investment_strategies/{user_risk_tolerance}_strategy.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(strategy)

    print(f"\n✅ Investment strategy saved to {filename}")
