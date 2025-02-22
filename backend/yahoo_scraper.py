import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime


def get_yahoo_finance_news(symbol: str, pages: int = 1) -> pd.DataFrame:
    """
    Scrape news headlines for a given stock symbol from Yahoo Finance.
    Args:
        symbol (str): Stock ticker (e.g. "AAPL").
        pages (int): Number of pages to scrape (Yahoo often paginates).
    Returns:
        pd.DataFrame: A dataframe with columns ["timestamp", "title", "url", "publisher"].
    """
    base_url = f"https://finance.yahoo.com/quote/{symbol.upper()}/news"
    all_articles = []

    for page in range(pages):
        # Start parameter for pagination. Each page is offset by multiples of 10 or 25 (depending on Yahoo’s structure).
        offset = page * 10
        url = f"{base_url}?offset={offset}&limit=10"

        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        if response.status_code != 200:
            print(
                f"Failed to retrieve page {page+1}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Each news item is often under <li> or <div> with a specific data-test or class name.
        # The structure may change over time. Adjust the selectors accordingly.
        news_items = soup.select('div#main div stream-container ul li')

        for item in news_items:
            # Title
            title_el = item.select_one('h3')
            if not title_el:
                continue
            title = title_el.get_text(strip=True)

            # URL
            link_el = title_el.find('a', href=True)
            if link_el:
                url_href = "https://finance.yahoo.com" + link_el['href']
            else:
                url_href = None

            # Publisher + Timestamp
            # Look for a <span> or <p> with metadata
            meta_el = item.select_one('div span + span')
            if meta_el:
                publisher = meta_el.get_text(strip=True)
            else:
                publisher = "N/A"

            # Sometimes there's a "data-time" attribute or "datetime" you can parse
            # For demonstration, we'll just store the scrape time.
            timestamp = datetime.datetime.utcnow().isoformat()

            all_articles.append({
                "timestamp": timestamp,
                "title": title,
                "url": url_href,
                "publisher": publisher
            })

    df = pd.DataFrame(all_articles)
    return df


if __name__ == "__main__":
    symbols = ["NEE", "FSLR"]
    for symbol in symbols:
        yahoo_df = get_yahoo_finance_news(symbol, pages=2)
        print(yahoo_df)
        yahoo_df.to_csv(
            f"./data/yahoo_scraped/yahoo_{symbol}_news.csv", index=False)
