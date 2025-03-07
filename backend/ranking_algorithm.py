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
import os

RISK_FREE_RATE = 0.044  # Assume 4.4% risk-free return (adjustable)


def build_stocks_metrics(stock: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Reads sentiment and financial metrics for a given stock and appends to df.

    Args:
        stock (str): Stock ticker symbol (e.g., "FSLR")
        df (pd.DataFrame): Existing DataFrame to append results to.

    Returns:
        pd.DataFrame: Updated DataFrame with stock metrics.
    """

    # Define file paths
    sentiment_file = f"./data/sentiment_scores/{stock}_sentiment_news.csv"
    financial_file = f"./advanced_metrics/{stock}_advanced_metrics.csv"

    # Initialize dictionary with default None values
    stock_data = {
        "ticker": stock,
        "sentiment_score": None,
        "ebitda": None,
        "five_yr_rev_cagr": None,
        "ev_ebitda": None,
        "roic": None,
        "fcf_yield": None,
        'implied_upside': None,
        'volatility': None,
        "sharpe_ratio": None,
    }

    # Load Sentiment Data
    if os.path.exists(sentiment_file):
        # Ensure proper header reading
        df_sent = pd.read_csv(sentiment_file, header=0)
        if not df_sent.empty and "sentiment_score_ranking" in df_sent.columns:
            stock_data["sentiment_score"] = df_sent["sentiment_score_ranking"].iloc[0]

    # Load Financial Data
    if os.path.exists(financial_file):
        # Ensure proper header reading
        df_fin = pd.read_csv(financial_file, header=0)

        if not df_fin.empty:
            # Ensure correct column names based on example CSV structure
            for col in ["ebitda", "five_yr_rev_cagr", "ev_ebitda", "roic", "fcf_yield", 'implied_upside', 'volatility']:
                if col in df_fin.columns:
                    stock_data[col] = df_fin[col].iloc[0]
                    print(f"added {col}")
                else:
                    print(
                        f"⚠️ Warning: Column '{col}' missing in {stock}'s CSV!")
        # Compute Sharpe Ratio
        if "implied_upside" in stock_data and "volatility" in stock_data:
            implied_upside = stock_data["implied_upside"]
            volatility = stock_data["volatility"]
            if volatility > 0:
                stock_data["sharpe_ratio"] = (
                    implied_upside - RISK_FREE_RATE) / volatility
            else:
                stock_data["sharpe_ratio"] = None  # Avoid division by zero

    # Convert dictionary to a properly formatted DataFrame
    new_row = pd.DataFrame([stock_data])

    # Ensure new_row matches df column structure before concatenation
    new_row = new_row[df.columns]

    # Append to existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    return df


def min_max_scale(series: pd.Series, invert=False) -> pd.Series:
    """
    Min-max scaling for normalization (0 to 1).
    If invert=True, reverses the scale (1 - min-max scaling).
    If all values are identical, assigns 0.5 to all entries.
    """
    if series.nunique() == 1:
        return pd.Series([0.5] * len(series), index=series.index)

    mn, mx = series.min(), series.max()
    scaled = (series - mn) / (mx - mn + 1e-9)

    return 1 - scaled if invert else scaled


def rank_stocks(
    df_factors: pd.DataFrame,
    w_sent=0.15,
    w_ebitda=0.15,
    w_rev=0.20,
    w_ev_ebitda=0.15,
    w_roic=0.15,
    w_fcf=0.20,
    w_sharpe=0.30
) -> pd.DataFrame:
    """
    Main function to produce a final ranking.
    Returns:
      A DataFrame with the final rank_score in descending order.
    """

    df_factors = df_factors[df_factors["implied_upside"]
                            is not None and df_factors["implied_upside"] > 0]
    df_rank = pd.DataFrame()

    df_rank['ticker'] = df_factors['ticker']

    # If some tickers have no articles => sent_score might be NaN => fill with 0.5 (neutral)
    df_factors["sentiment_score"].fillna(
        0.5, inplace=True)
    df_rank['sentiment_score'] = df_factors["sentiment_score"]

    # ==============================
    # 3) Scale the other factors
    # ==============================
    # ebitda => higher is better => min-max
    df_rank["ebitda_scaled"] = min_max_scale(df_factors["ebitda"])

    # revCAGR5 => 5yr revenue CAGR => higher is better => min-max
    df_rank["revCAGR5_scaled"] = min_max_scale(
        df_factors["five_yr_rev_cagr"])

    # ev_ebitda => lower is better => invert it after min-max
    # We'll do scaled_ev_ebitda = 1 - min_max_scale(ev_ebitda)
    # If ev_ebitda is missing, fill with median or something
    df_factors["ev_ebitda"].fillna(
        df_factors["ev_ebitda"].median(), inplace=True)
    df_rank["ev_ebitda_scaled"] = min_max_scale(
        df_factors["ev_ebitda"], invert=True)

    # roic => higher is better => min-max
    df_rank["roic_scaled"] = min_max_scale(df_factors["roic"])

    # fcf_yield => higher is better => min-max
    df_rank["fcf_yield_scaled"] = min_max_scale(df_factors["fcf_yield"])

    # Normalize implied upside (higher is better)
    df_rank["sharpe_ratio_scaled"] = min_max_scale(
        df_factors["sharpe_ratio"])

    df_rank.fillna(0, inplace=True)
    # ==============================
    # 4) Compute final rank_score
    # ==============================
    df_rank["rank_score"] = (
        w_sent * df_rank["sentiment_score"] +
        w_ebitda * df_rank["ebitda_scaled"] +
        w_rev * df_rank["revCAGR5_scaled"] +
        w_ev_ebitda * df_rank["ev_ebitda_scaled"] +
        w_roic * df_rank["roic_scaled"] +
        w_fcf * df_rank["fcf_yield_scaled"] +
        w_sharpe * df_rank["sharpe_ratio_scaled"]
    )

    df_rank['implied_upside'] = df_factors['implied_upside']
    df_rank['volatility'] = df_factors['volatility']
    df_rank['sharpe_ratio'] = df_factors['sharpe_ratio']

    # ==============================
    # 5) Sort descending
    # ==============================
    df_rank = df_rank.sort_values(
        "rank_score", ascending=False)
    df_rank['rank'] = range(1, len(df_rank) + 1)

    return df_rank.reset_index(drop=True)


if __name__ == "__main__":

    SYMBOLS = ["NEE", "FSLR", "ENPH", "RUN", "SEDG",
               "CSIQ", "JKS", "NXT", "SPWR", "DQ", "ARRY", "NEP", "GE", "VWS", "IBDRY", "DNNGY", 'BEP', "NPI", "CWEN", "INOXWIND", "ORA", "IDA", "OPTT", "DRXGY", "EVA", "GPRE", "PLUG", "BE", "BLDP", "ARL", "OPTT", "CEG", "VST", "CCJ", "LEU", "SMR", "OKLO", "NNE", "BWXT", "BW", "TLNE"]
    df_stocks = pd.DataFrame(columns=[
        'ticker', 'sentiment_score', 'ebitda', 'five_yr_rev_cagr', 'ev_ebitda', 'roic', 'fcf_yield', 'implied_upside', 'volatility', 'sharpe_ratio'])
    for symbol in SYMBOLS:
        df_stocks = build_stocks_metrics(symbol, df_stocks)

    df_ranked = rank_stocks(df_stocks)
    df_ranked.to_csv("./stocks_ranked.csv")
