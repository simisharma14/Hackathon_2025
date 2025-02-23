import openai
import os
import csv
import glob
import pandas as pd
from dotenv import load_dotenv
from sentiment_analysis import add_finbert_sentiment
from macro_outlook_scraper import get_polygon_news
from federal_register_scraper import get_federal_register_docs

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_and_analyze_news():
    """
    Fetches macroeconomic and regulatory news and applies sentiment analysis.
    Returns:
        pd.DataFrame: DataFrame containing sentiment-analyzed news.
    """
    print("Fetching macro and regulatory news...")
    macro_news = get_polygon_news(
        "energy", os.getenv("POLYGON_API_KEY"), limit=50)
    regulatory_news = get_federal_register_docs(
        "energy policies", per_page=20, max_pages=5)

    all_news = pd.concat([macro_news, regulatory_news], ignore_index=True)

    if all_news.empty:
        return None

    print("Applying sentiment analysis...")
    return add_finbert_sentiment(all_news)


openai.api_key = os.getenv("OPENAI_API_KEY")


def read_entire_csv_folder(folder_path):
    """
    Reads all CSV files in `folder_path` in their entirety
    and returns a combined text summary of *all* contents.

    WARNING: This can become *very large* if the CSV files are big,
    potentially leading to prompt size issues.
    """
    summary_lines = []
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

    for csv_file in csv_files:
        summary_lines.append(f"--- File: {os.path.basename(csv_file)} ---")
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header:
                    summary_lines.append(f"Header: {header}")
                row_index = 0
                for row in reader:
                    row_index += 1
                    summary_lines.append(f"Row {row_index}: {row}")
        except Exception as e:
            summary_lines.append(f"Error reading {csv_file}: {str(e)}")

    return "\n".join(summary_lines)


# def generate_macro_outlook(regulatory_text, macro_news_text):
#     """
#     Creates a prompt that includes the CSV data at the top, then the main instructions.
#     """
#     combined_csv_summary = (
#         "Recent Regulatory Data (excerpted from CSVs):\n"
#         f"{regulatory_text}\n\n"
#         "Recent Macro/Energy News (excerpted from CSVs):\n"
#         f"{macro_news_text}\n\n"
#     )

#     instructions = (
#         "Use the csv summary I gave you with current news to put an emphasis on relavant current events in the energy sector and talk about quantitiative information"
#         "Also use your information on current events to add to this data and give a very current, up to date overview of what is going on with clean and nuclear energy"
#         "Be very professional and financial"
#         "But emphasis on key takeaways and economic indicators moving foward"
#     )

#     prompt = combined_csv_summary + instructions

def generate_macro_outlook():
    """
    Generates a comprehensive macro outlook report for the energy sector
    by incorporating sentiment analysis from macroeconomic and regulatory news.
    """

    # =============================
    # Step 1: Fetch Macro & Regulatory News
    # =============================
    print("Fetching macroeconomic and regulatory news...")
    df_macro_news = get_polygon_news(
        "energy", api_key=os.getenv("POLYGON_API_KEY"), limit=30)

    # Define keywords for regulatory news
    SYMBOLS = ["clean energy", "renewable energy", "energy efficiency", "nuclear energy", "nuclear regulation",
               "solar energy", "solar power", "wind power", "wind energy", "hydropower", "geothermal", "climate change"]

    df_regulatory_news = pd.DataFrame()
    for symbol in SYMBOLS:
        temp_df = get_federal_register_docs(symbol)
        df_regulatory_news = pd.concat(
            [df_regulatory_news, temp_df], ignore_index=True)

    if df_macro_news.empty and df_regulatory_news.empty:
        return "No relevant macroeconomic or regulatory news found."

    # =============================
    # Step 2: Apply Sentiment Analysis
    # =============================
    if not df_macro_news.empty:
        df_macro_news = add_finbert_sentiment(df_macro_news)
        df_macro_news["net_sentiment"] = df_macro_news["prob_positive"] - \
            df_macro_news["prob_negative"]
        macro_sentiment_score = df_macro_news["net_sentiment"].mean()
    else:
        macro_sentiment_score = None

    if not df_regulatory_news.empty:
        df_regulatory_news = add_finbert_sentiment(df_regulatory_news)
        df_regulatory_news["net_sentiment"] = df_regulatory_news["prob_positive"] - \
            df_regulatory_news["prob_negative"]
        regulatory_sentiment_score = df_regulatory_news["net_sentiment"].mean()
    else:
        regulatory_sentiment_score = None

    # =============================
    # Step 3: Aggregate Sentiment Data
    # =============================
    sentiment_summary = ""
    if macro_sentiment_score is not None:
        sentiment_summary += f"Macroeconomic sentiment score: {macro_sentiment_score:.2f}\n"
    if regulatory_sentiment_score is not None:
        sentiment_summary += f"Regulatory sentiment score: {regulatory_sentiment_score:.2f}\n"

    sentiment_summary += (
        "A positive sentiment score indicates optimism in the energy sector, while a negative score suggests concerns "
        "over policy changes, economic uncertainty, or regulatory risks."
    )

    # =============================
    # Step 4: Generate Macro Outlook Using OpenAI
    # =============================
    prompt = (
        "Write a detailed macro outlook report for the energy sector, incorporating the following sentiment analysis data:\n\n"
        f"{sentiment_summary}\n\n"
        "Include discussions on renewable energy, nuclear, solar, wind, hydropower, and geothermal trends. "
        "Analyze recent regulatory changes, government policies, and market trends. Highlight potential future challenges and opportunities. "
        "Discuss how the sentiment trends may impact investment decisions in the clean energy sector. Use markdown syntax to make nice and clear sections and bullet points. Be extremely thorough."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use GPT-4 for better insights
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1200
    )

    outlook_report = response["choices"][0]["message"]["content"]

    return outlook_report


def save_report(report, filename):
    """
    Saves the generated report to a file.
    """
    os.makedirs("./data/ai_reports", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Saved macro outlook report to {filename}")


def main():
    """
    Generates and saves the macro outlook report.
    """
    outlook_report = generate_macro_outlook()
    print("Macro Outlook Report:")
    print(outlook_report)
    save_report(outlook_report, "./data/ai_reports/macro_outlook_report.txt")


if __name__ == "__main__":
    main()
