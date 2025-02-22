import pandas as pd


def aggregate_sentiment(ticker) -> pd.DataFrame:
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
    try:
        df_articles = pd.read_csv(
            f"./data/sentiment_scores/{ticker}_sentiment_news.csv")

        print(f"Correctly read {symbol} sentiment scores")
        df_articles["net_sentiment"] = df_articles["prob_positive"] - \
            df_articles["prob_negative"]
        df_articles["average_sentiment"] = df_articles["net_sentiment"].mean(
        )
        df_articles["sentiment_score_ranking"] = (
            df_articles["average_sentiment"] + 1) / 2.0

        df_articles.to_csv(
            f"./data/sentiment_scores/{ticker}_sentiment_news.csv")
    except Exception as e:
        print(f"Error reading {symbol} sentiment scores")


SYMBOLS = ["NEE", "FSLR", "ENPH", "RUN", "SEDG",
           "CSIQ", "JKS", "NXT", "SPWR", "DQ", "ARRY", "NEP", "GE", "VWS", "IBDRY", "DNNGY", 'BEP', "NPI", "CWEN", "INOXWIND", "ORA", "IDA", "OPTT", "DRXGY", "EVA", "GPRE", "PLUG", "BE", "BLDP", "ARL", "OPTT", "CEG", "VST", "CCJ", "LEU", "SMR", "OKLO", "NNE", "BWXT", "BW", "TLNE"
           ]

for symbol in SYMBOLS:
    aggregate_sentiment(symbol)
