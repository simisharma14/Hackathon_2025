"""
ranking_algorithm.py

A standalone Python script demonstrating a multi-factor ranking system using:
- Article-level sentiment probabilities (pos, neu, neg)
- EBITDA
- 5-year Revenue CAGR (revCAGR5)
- EV/EBITDA
- ROIC
- FCF Yield

Steps:
1) Aggregate sentiment from df_articles.
2) Merge with df_factors containing fundamentals.
3) Normalize each factor 0..1 (or invert if lower-is-better).
4) Weighted sum => final rank_score.
5) Sort descending => final ranking.
"""

import pandas as pd


def aggregate_sentiment(df_articles: pd.DataFrame) -> pd.DataFrame:
    """
    Given a DataFrame with columns:
      [ticker, p_pos, p_neu, p_neg]
    we compute a net sentiment per article => net_sent = p_pos - p_neg
    Then group by ticker to find avg_sentiment => mean of net_sent.

    Returns a DataFrame with:
      [ticker, avg_sentiment, sent_score]
    where avg_sentiment is in [-1, +1],
    and sent_score is in [0, 1] after transformation.
    """
    # 1) Compute net_sentiment for each article
    df_articles["net_sentiment"] = df_articles["prob_positive"] - \
        df_articles["prob_negative"]

    # 2) Group by ticker, average net_sent
    df_agg = df_articles.groupby(
        "ticker")["net_sentiment"].mean().reset_index()
    df_agg.rename(columns={"net_sentiment": "avg_sentiment"}, inplace=True)

    # 3) Convert [-1..+1] to [0..1]
    df_agg["sentiment_score"] = (df_agg["avg_sentiment"] + 1) / 2.0

    return df_agg[["ticker", "avg_sentiment", "sentiment_score"]]


def min_max_scale(series: pd.Series) -> pd.Series:
    """
    Standard min-max scaling to [0..1].
    If all values are the same, we return 0.5 for all to avoid division by zero.
    """
    if series.nunique() == 1:
        return pd.Series([0.5] * len(series), index=series.index)
    mn, mx = series.min(), series.max()
    return (series - mn) / (mx - mn + 1e-9)


def rank_stocks(
    df_articles: pd.DataFrame,
    df_factors: pd.DataFrame,
    w_sent=0.10,
    w_ebitda=0.15,
    w_rev=0.20,
    w_ev_ebitda=0.15,
    w_roic=0.20,
    w_fcf=0.20
) -> pd.DataFrame:
    """
    Main function to produce a final ranking.

    Inputs:
      - df_articles: columns [ticker, p_pos, p_neu, p_neg]
      - df_factors: columns [ticker, ebitda, revCAGR5, ev_ebitda, roic, fcf_yield]
      - Weights: w_sent, w_ebitda, w_rev, w_ev_ebitda, w_roic, w_fcf

    Returns:
      A DataFrame with the final rank_score in descending order.
    """

    # ==============================
    # 1) Aggregate Sentiment
    # ==============================
    df_sents = aggregate_sentiment(df_articles)
    # df_sents has [ticker, avg_sentiment, sent_score]

    # ==============================
    # 2) Merge with df_factors
    # ==============================
    df_merged = pd.merge(df_factors, df_sents, on="ticker", how="left")

    # If some tickers have no articles => sent_score might be NaN => fill with 0.5 (neutral)
    df_merged["sent_score"].fillna(0.5, inplace=True)

    # ==============================
    # 3) Scale the other factors
    # ==============================
    # ebitda => higher is better => min-max
    df_merged["ebitda_scaled"] = min_max_scale(df_merged["ebitda"])

    # revCAGR5 => 5yr revenue CAGR => higher is better => min-max
    df_merged["revCAGR5_scaled"] = min_max_scale(df_merged["revCAGR5"])

    # ev_ebitda => lower is better => invert it after min-max
    # We'll do scaled_ev_ebitda = 1 - min_max_scale(ev_ebitda)
    # If ev_ebitda is missing, fill with median or something
    df_merged["ev_ebitda"].fillna(
        df_merged["ev_ebitda"].median(), inplace=True)
    df_merged["ev_ebitda_scaled"] = 1 - min_max_scale(df_merged["ev_ebitda"])

    # roic => higher is better => min-max
    df_merged["roic_scaled"] = min_max_scale(df_merged["roic"])

    # fcf_yield => higher is better => min-max
    df_merged["fcf_yield_scaled"] = min_max_scale(df_merged["fcf_yield"])

    # ==============================
    # 4) Compute final rank_score
    # ==============================
    df_merged["rank_score"] = (
        w_sent * df_merged["sent_score"] +
        w_ebitda * df_merged["ebitda_scaled"] +
        w_rev * df_merged["revCAGR5_scaled"] +
        w_ev_ebitda * df_merged["ev_ebitda_scaled"] +
        w_roic * df_merged["roic_scaled"] +
        w_fcf * df_merged["fcf_yield_scaled"]
    )

    # ==============================
    # 5) Sort descending
    # ==============================
    df_ranked = df_merged.sort_values(
        "rank_score", ascending=False).reset_index(drop=True)

    return df_ranked


# ==============================
# Example Main Usage
# ==============================
if __name__ == "__main__":

    # EXAMPLE df_articles with columns: ticker, p_pos, p_neu, p_neg
    df_articles = pd.DataFrame({
        "ticker": ["AAPL", "AAPL", "MSFT", "GOOG", "GOOG"],
        "p_pos": [0.7, 0.6, 0.8, 0.2, 0.4],
        "p_neu": [0.2, 0.3, 0.1, 0.6, 0.3],
        "p_neg": [0.1, 0.1, 0.1, 0.2, 0.3],
    })

    # EXAMPLE df_factors with columns: ticker, ebitda, revCAGR5, ev_ebitda, roic, fcf_yield
    df_factors = pd.DataFrame({
        "ticker": ["AAPL", "MSFT", "GOOG", "AMZN"],
        "ebitda": [100e9, 80e9, 65e9, 50e9],
        "revCAGR5": [0.15, 0.12, 0.10, 0.25],
        "ev_ebitda": [22.5, 18.0, 20.0, 30.0],
        "roic": [0.25, 0.18, 0.22, 0.05],
        "fcf_yield": [0.04, 0.03, 0.02, 0.01],
    })

    # Example usage:
    df_ranked = rank_stocks(df_articles, df_factors)
    print("\nFinal Ranking:")
    print(df_ranked[["ticker", "rank_score", "sent_score", "ebitda_scaled",
          "revCAGR5_scaled", "ev_ebitda_scaled", "roic_scaled", "fcf_yield_scaled"]])
