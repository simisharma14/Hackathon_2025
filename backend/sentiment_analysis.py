from transformers import pipeline
from polygon_scraper import get_polygon_news
import pandas as pd
import datetime


def convert_iso_to_mm_dd_yyyy(iso_str):
    """
    Convert an ISO timestamp (e.g. '2024-06-28T15:43:00Z')
    to 'MM-DD-YYYY'. If parsing fails, return the original string.
    """
    if not isinstance(iso_str, str):
        return iso_str
    try:
        dt = datetime.datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%m-%d-%Y")
    except ValueError:
        return iso_str


def add_finbert_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each row in df["title"], run FinBERT sentiment analysis and
    append 'prob_positive', 'prob_neutral', 'prob_negative',
    as well as the top sentiment label.
    """
    # 1) Load the FinBERT model in "return_all_scores" mode
    sentiment_pipeline = pipeline(
        "text-classification",
        model="ProsusAI/finbert",
        return_all_scores=True
    )

    # Lists to store results
    top_labels = []
    top_scores = []
    pos_probs = []
    neu_probs = []
    neg_probs = []

    for title in df["title"]:
        # Handle empty or missing titles gracefully
        if not isinstance(title, str) or not title.strip():
            top_labels.append("neutral")
            top_scores.append(0.0)
            pos_probs.append(0.0)
            neu_probs.append(1.0)
            neg_probs.append(0.0)
            continue

        # 2) Get probability distribution for all labels
        # Example structure:
        # [
        #   {"label": "positive", "score": 0.75},
        #   {"label": "neutral",  "score": 0.20},
        #   {"label": "negative", "score": 0.05}
        # ]
        results = sentiment_pipeline(title)[0]

        # Convert list of dicts into a dict by label
        prob_dict = {r["label"].lower(): r["score"] for r in results}

        # Extract each probability
        positive_score = prob_dict.get("positive", 0.0)
        neutral_score = prob_dict.get("neutral", 0.0)
        negative_score = prob_dict.get("negative", 0.0)

        # Determine top label and score
        label_scores = [
            ("positive", positive_score),
            ("neutral",  neutral_score),
            ("negative", negative_score)
        ]
        # Sort by highest score
        top_label, max_score = max(label_scores, key=lambda x: x[1])

        # Append to lists
        top_labels.append(top_label)
        top_scores.append(max_score)
        pos_probs.append(positive_score)
        neu_probs.append(neutral_score)
        neg_probs.append(negative_score)

    # 3) Insert new columns into DataFrame
    df["sentiment"] = top_labels
    df["score"] = top_scores
    df["prob_positive"] = pos_probs
    df["prob_neutral"] = neu_probs
    df["prob_negative"] = neg_probs

    return df


if __name__ == "__main__":
    POLYGON_API_KEY = "4cR_irLDgivxae1WO4y0Wb30VYxXRkQj"
    SYMBOLS = ["NEE", "FSLR"]

    for symbol in SYMBOLS:
        # Step 1: Fetch news
        df_news = get_polygon_news(symbol, api_key=POLYGON_API_KEY, limit=20)

        # Convert ISO timestamps to MM-DD-YYYY
        if "timestamp" in df_news.columns:
            df_news["timestamp"] = df_news["timestamp"].apply(
                convert_iso_to_mm_dd_yyyy)

        print(f"\n=== Raw Data for {symbol} ===")
        print(df_news.head())

        # Step 2: Apply FinBERT sentiment
        if not df_news.empty:
            df_with_sentiment = add_finbert_sentiment(df_news)
            print(f"\n=== Sentiment Data for {symbol} ===")
            print(df_with_sentiment.head())

            # Save to CSV
            out_path = f"./data/sentiment_scores/{symbol}_sentiment_news.csv"
            df_with_sentiment.to_csv(out_path, index=False)
            print(f"Saved sentiment analysis to {out_path}")
