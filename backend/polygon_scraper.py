import requests
import pandas as pd
from datetime import datetime, timedelta


def convert_iso_to_mm_dd_yyyy(iso_str):
    """
    Convert an ISO timestamp (e.g. '2024-06-28T15:43:00Z')
    to 'MM-DD-YYYY'. If parsing fails, return the original string.
    """
    if not isinstance(iso_str, str):
        return iso_str
    try:
        dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%m-%d-%Y")
    except ValueError:
        return iso_str


def get_polygon_news(symbol: str, api_key: str, limit: int = 50) -> pd.DataFrame:
    """
    Fetch recent news articles from Polygon for a given stock symbol.

    Args:
        symbol (str): Stock ticker symbol (e.g. "AAPL").
        api_key (str): Polygon.io API key.
        limit (int): Max number of articles to fetch.

    Returns:
        pd.DataFrame: A dataframe with columns ["timestamp", "title", "url", "source"].
                      Only articles from the last 30 days are included.
    """
    base_url = "https://api.polygon.io/v2/reference/news"
    params = {
        "ticker": symbol.upper(),
        "limit": limit,
        "apiKey": api_key
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "results" not in data:
        print("No news found or invalid API response.")
        return pd.DataFrame()

    # Get today's date and 30-day threshold
    today = datetime.now()
    cutoff_date = today - timedelta(days=30)

    articles = []

    for item in data["results"]:
        published_utc = item.get("published_utc")
        formatted_date = convert_iso_to_mm_dd_yyyy(published_utc)

        if formatted_date is None:
            continue  # Skip if date conversion fails

        # Convert back to datetime for filtering
        article_date = datetime.strptime(formatted_date, "%m-%d-%Y")

        # Include only articles from the last 30 days
        if article_date >= cutoff_date:
            articles.append({
                "timestamp": formatted_date,
                "title": item.get("title"),
                "url": item.get("article_url"),
                "source": item.get("publisher", {}).get("name", "Unknown")
            })

    # Convert to DataFrame
    df = pd.DataFrame(articles)

    return df


if __name__ == "__main__":
    API_KEY = "4cR_irLDgivxae1WO4y0Wb30VYxXRkQj"

    SYMBOLS = ["NEE", "FSLR", "ENPH", "RUN", "SEDG",
               "CSIQ", "JKS", "NXT", "SPWR", "DQ", "ARRY", "NEP", "GE", "VWS", "IBDRY", "DNNGY", 'BEP', "NPI", "CWEN", "INOXWIND", "ORA", "IDA", "OPTT", "DRXGY", "EVA", "GPRE", "PLUG", "BE", "BLDP", "ARL", "OPTT", "CEG", "VST", "CCJ", "LEU", "SMR", "OKLO", "NNE", "BWXT", "BW", "TLNE"
               ]
    # SYMBOLS = ["FSLR", "NEE"]
    ETFS = ["NLR", "TAN", "FAN", "ICLN", "PBW", "HYDR", "NLR"]
    for symbol in SYMBOLS:
        print(f"Fetching news for {symbol}")
        polygon_df = get_polygon_news(symbol, API_KEY, limit=50)
        if "timestamp" in polygon_df.columns:
            polygon_df["timestamp"] = polygon_df["timestamp"].apply(
                convert_iso_to_mm_dd_yyyy)
        polygon_df.to_csv(
            f"./data/polygon_scraped/{symbol}_news.csv", index=False)
