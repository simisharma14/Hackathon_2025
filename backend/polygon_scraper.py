import requests
import pandas as pd
import datetime


def get_polygon_news(symbol: str, api_key: str, limit: int = 50) -> pd.DataFrame:
    """
    Fetch recent news articles from Polygon for a given stock symbol.
    Args:
        symbol (str): Stock ticker symbol (e.g. "AAPL").
        api_key (str): Polygon.io API key.
        limit (int): Max number of articles to fetch (Polygon will paginate).
    Returns:
        pd.DataFrame: A dataframe with columns ["timestamp", "title", "url", "source"].
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

    articles = []

    for item in data["results"]:
        # Each item typically has "published_utc", "title", "article_url", and "source"
        articles.append({
            "timestamp": item.get("published_utc"),
            "title": item.get("title"),
            "url": item.get("article_url"),
            "source": item.get("publisher").get("name")
        })

    df = pd.DataFrame(articles)
    return df


if __name__ == "__main__":
    API_KEY = "4cR_irLDgivxae1WO4y0Wb30VYxXRkQj"

    symbols = ["NEE", "FSLR"]
    for symbol in symbols:
        polygon_df = get_polygon_news(symbol, API_KEY, limit=50)
        print(polygon_df)
        polygon_df.to_csv(
            f"./data/polygon_scraped/polygon_{symbol}_news.csv", index=False)
