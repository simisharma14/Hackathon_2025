import pandas as pd


def aggregate_sentiment(ticker) -> pd.DataFrame:
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
