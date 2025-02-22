import os
import requests
import pandas as pd
from datetime import datetime
import yfinance as yf
import numpy as np
from dotenv import load_dotenv

load_dotenv()


def compute_sma(series: pd.Series, window: int) -> pd.Series:
    """
    Compute Simple Moving Average (SMA) over a given window.
    """
    return series.rolling(window=window).mean()


def compute_rsi(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """
    Compute the RSI for the given price column using the standard approach.
    RSI formula:
       1) delta = diff of prices
       2) up = positive gains, down = negative gains
       3) use exponential moving average (ewm) for up and down
       4) rs = ema_up / ema_down
       5) rsi = 100 - (100 / (1 + rs))
    """
    delta = df[column].diff()

    # Separate positive and negative moves
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)

    # Exponential moving average of ups and downs
    ema_up = up.ewm(span=period, adjust=False).mean()
    ema_down = down.ewm(span=period, adjust=False).mean()

    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def pull_historical_data_polygon_all_time(symbol: str, api_key: str, save_path: str = "./company_profiles"):
    """
    Pulls daily OHLC data (and computes SMA-50, SMA-200, RSI-14) for the entire available date range
    from Polygon.io for the given ticker symbol.
    
    The function uses a fallback start date (e.g. "2000-01-01") so that if you do not specify
    start/end, it attempts to pull as much history as possible.
    """
    # Set fallback start date and today's date as end date
    start = "2000-01-01"
    end = datetime.today().strftime("%Y-%m-%d")
    
    os.makedirs(save_path, exist_ok=True)
    output_data = {}

    ohlc_url = f"https://api.polygon.io/v2/aggs/ticker/{symbol.upper()}/range/1/day/{start}/{end}"
    params = {
        "adjusted": "true",
        "sort": "desc",
        "limit": 50000,
        "apiKey": api_key
    }
    
    try:
        response = requests.get(ohlc_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[Error] Failed to fetch OHLC data for {symbol}: {e}")
        return None

    if data.get("resultsCount", 0) == 0:
        print(f"[Warning] No data found for {symbol} between {start} and {end}.")
        return None

    # Create a DataFrame from the results
    bars = data["results"]
    df_bars = pd.DataFrame(bars)

    # Rename columns to standard names
    df_bars.rename(columns={
        "t": "timestamp",
        "o": "open",
        "h": "high",
        "l": "low",
        "c": "close",
        "v": "volume"
    }, inplace=True)

    # Convert the timestamp (milliseconds) to datetime
    df_bars["timestamp"] = pd.to_datetime(df_bars["timestamp"], unit="ms")
    df_bars.sort_values("timestamp", inplace=True)
    df_bars.reset_index(drop=True, inplace=True)

    # Compute the technical indicators:
    df_bars["SMA_50"] = compute_sma(df_bars["close"], 50)
    df_bars["SMA_200"] = compute_sma(df_bars["close"], 200)

    # For RSI, set the index to timestamp temporarily
    df_bars.set_index("timestamp", inplace=True)
    df_bars["RSI_14"] = compute_rsi(df_bars, column="close", period=14)
    df_bars.reset_index(inplace=True)

    # Reorder columns as desired
    desired_order = ["timestamp", "volume", "open", "close", "high", "low", "SMA_50", "SMA_200", "RSI_14"]
    try:
        df_out = df_bars[desired_order]
    except KeyError as e:
        print(f"[Error] Missing expected columns for {symbol}: {e}")
        df_out = df_bars

    # Save the final DataFrame to CSV
    out_file = os.path.join(save_path, f"{symbol}_technical_all_time.csv")
    df_out.to_csv(out_file, index=False)
    print(f"[+] Saved Yahoo Finance technical data for {symbol} to {out_file}")

    output_data["tech_data"] = df_out
    return output_data



def pull_technical_data_yf(symbol: str, save_path: str = "./company_profiles2"):

    os.makedirs(save_path, exist_ok=True)
    ticker = yf.Ticker(symbol)
    hist = ticker.history()  # full available history

    if hist.empty:
        print(f"[Error] No historical data available for {symbol}.")
        return None

    available_start = hist.index.min().strftime("%Y-%m-%d")
    available_end = hist.index.max().strftime("%Y-%m-%d")
    print(f"[Info] Data available for {symbol} from {available_start} to {available_end}.")
    # Reset index to get Date as a column
    hist.reset_index(inplace=True)

    # Rename columns to lowercase and standard names
    hist.rename(columns={
        "Date": "timestamp",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)


    # Compute technical indicators on the 'close' price
    hist["SMA_50"] = compute_sma(hist["close"], 50)
    hist["SMA_200"] = compute_sma(hist["close"], 200)
    hist["RSI_14"] = compute_rsi(hist, column="close", period=14)

    # Reorder columns as desired:
    desired_order = ["timestamp", "volume", "open", "close", "high", "low", "SMA_50", "SMA_200", "RSI_14"]
    df_out = hist[desired_order]

    # Save the resulting DataFrame to CSV
    out_path = os.path.join(save_path, f"{symbol}_technical_yf.csv")
    df_out.to_csv(out_path, index=False)
    print(f"[+] Saved Yahoo Finance technical data for {symbol} to {out_path}")
    
    return df_out


def pull_financial_statements(symbol: str, save_path: str = "./financial_statements"):

    os.makedirs(save_path, exist_ok=True)

    try:
        stock = yf.Ticker(symbol)
        # row = {col: None for col in CSV_COLUMNS}
        info = stock.info
    except Exception as e:
        print(f"[Error] Could not retrieve .info for {symbol}: {e}")
        return

    if not info:
        print(
            f"[Warning] No 'info' returned for {symbol}. Possibly an invalid ticker.")
        return

    '''
    # Fill the easy ones:
    row["ticker"] = symbol.upper()
    row["company_name"] = info.get("shortName", None)
    row["fiscal_year"] = None
    row["fiscal_period"] = None
    row["start_date"] = None
    row["end_date"] = None
    row["filing_date"] = None
    '''

    try:
        balance_sheet = stock.balance_sheet  # Annual balance sheet
        income_statement = stock.financials  # Annual income statement
        cash_flow = stock.cashflow  # Annual cash flow statement
    except Exception as e:
        print(
            f"[Error] Could not retrieve financial statements for {symbol}: {e}")
        return

    if not balance_sheet.empty:
        balance_sheet.to_csv(
            os.path.join(save_path, f"{symbol}_balance_sheet.csv"))
    else:
        print(f"No balance sheet data found for {symbol}.")

    if not income_statement.empty:
        income_statement.to_csv(
            os.path.join(save_path, f"{symbol}_income_statement.csv"))
    else:
        print(f"No income statement data found for {symbol}.")

    if not cash_flow.empty:
        cash_flow.to_csv(
            os.path.join(save_path, f"{symbol}_cash_flow.csv"))
    else:
        print(f"No cash flow data found for {symbol}.")


def pull_financial_overview(symbol: str, save_path: str = "./financial_overviews"):

    os.makedirs(save_path, exist_ok=True)

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
    except Exception as e:
        print(f"[Error] Could not retrieve info for {symbol}: {e}")
        return

    if not info:
        print(f"[Warning] No overview info for {symbol}. Skipping.")
        return

    # 3) Grab each metric (use .get() to avoid KeyErrors)
    market_cap = info.get("marketCap")
    day_high = info.get("dayHigh")
    day_low = info.get("dayLow")
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")
    previous_close = info.get("previousClose")
    open_price = info.get("open")
    beta_val = info.get("beta")

    # For P/E ratio, we'll prefer trailingPE if present, otherwise forwardPE
    p_e = info.get("trailingPE")
    if p_e is None:
        p_e = info.get("forwardPE")

    # 4) Build a single dict row
    row = {
        "symbol": symbol.upper(),
        "market_cap": market_cap,
        "day_high": day_high,
        "day_low": day_low,
        "52wk_high": fifty_two_week_high,
        "52wk_low": fifty_two_week_low,
        "previous_close": previous_close,
        "open": open_price,
        "beta": beta_val,
        "p_e_ratio": p_e
    }

    # 5) Create a DataFrame with one row
    df = pd.DataFrame([row])
    df1 = df.T.reset_index()
    df1.columns = ["Metric", "Value"]

    # 6) Save to CSV named '{symbol}_overview.csv'
    out_file = os.path.join(save_path, f"{symbol}_overview.csv")
    df1.to_csv(out_file, index=False)
    print(f"[+] Saved financial overview for {symbol} to: {out_file}")


def compute_5yr_cagr(revenue_series: pd.Series) -> float:
    revenue_series = revenue_series.astype(float)
    if len(revenue_series) < 5:
        start_val = revenue_series.iloc[0]
        end_val = revenue_series.iloc[-1]
    else:
        start_val = revenue_series.iloc[-5]
        end_val = revenue_series.iloc[-1]
    # Number of intervals = (# of data points - 1)
    periods = len(revenue_series) - 1
    if start_val <= 0:
        return None
    cagr = (end_val / start_val) ** (1.0 / periods) - 1
    return cagr


def pull_advanced_metrics(symbol: str, save_path: str = "./advanced_metrics"):
    os.makedirs(save_path, exist_ok=True)

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
    except Exception as e:
        print(f"[Error] Could not retrieve info for {symbol}: {e}")
        return

    if not info:
        print(f"[Warning] No overview info for {symbol}. Skipping.")
        return

    annual_fin = ticker.financials

    annual_bs = ticker.balance_sheet

    metrics = {
        "symbol": symbol.upper(),
        "ebitda": None,
        "five_yr_rev_cagr": None,
        "ev_ebitda": None,
        "roic": None,
        "fcf_yield": None,
        "implied_upside": None,
        "volatility": None,
    }

    ebitda_val = info.get("ebitda")
    metrics["ebitda"] = ebitda_val

    if (annual_fin is not None) and (not annual_fin.empty):
        if "Total Revenue" in annual_fin.index:
            # Ascending by column date
            rev_row = annual_fin.loc["Total Revenue"].sort_index()
            rev_row.dropna(inplace=True)
            if len(rev_row) >= 2:
                metrics["five_yr_rev_cagr"] = compute_5yr_cagr(rev_row)

    ev = info.get("enterpriseValue")
    if ev and ebitda_val and ebitda_val != 0:
        metrics["ev_ebitda"] = ev / ebitda_val

    net_income = None
    if (annual_fin is not None) and ("Net Income" in annual_fin.index):
        ni_row = annual_fin.loc["Net Income"].sort_index().dropna()
        if not ni_row.empty:
            net_income = ni_row.iloc[-1]  # The most recent annual net income

    # For equity and debt, let's see if annual_bs has them
    equity = 0
    total_debt = 0
    if (annual_bs is not None) and (not annual_bs.empty):
        if "Total Stockholder Equity" in annual_bs.index:
            eq_row = annual_bs.loc["Total Stockholder Equity"].sort_index(
            ).dropna()
            if not eq_row.empty:
                equity = eq_row.iloc[-1]
        if "Long Term Debt" in annual_bs.index:
            lt_debt_row = annual_bs.loc["Long Term Debt"].sort_index().dropna()
            if not lt_debt_row.empty:
                total_debt += lt_debt_row.iloc[-1]
        if "Short Long Term Debt" in annual_bs.index:
            st_debt_row = annual_bs.loc["Short Long Term Debt"].sort_index(
            ).dropna()
            if not st_debt_row.empty:
                total_debt += st_debt_row.iloc[-1]

    roic_val = None
    denom = equity + total_debt
    if net_income and denom != 0:
        roic_val = net_income / denom
    metrics["roic"] = roic_val

    fcf = info.get("freeCashflow")
    mcap = info.get("marketCap")
    fcf_yield_val = None
    if fcf and mcap and mcap != 0:
        fcf_yield_val = fcf / mcap
    metrics["fcf_yield"] = fcf_yield_val

    # Compute implied upside
    try:
        current_price = info.get("currentPrice")
        if ebitda_val and total_debt is not None and current_price is not None:
            # Compute Enterprise Value (EV)
            # Compute Equity Value
            equity_value = ev - total_debt
            # Compute Target Price
            target_price = equity_value / info.get("sharesOutstanding")
            # Compute Implied Upside
            metrics["implied_upside"] = (
                (target_price - current_price) / current_price)
    except Exception as e:
        print(f"[Error] Could not calculate implied upside for {symbol}: {e}")

    try:
        # Calculate historical volatility
        hist_prices = ticker.history(
            start="2024-01-01", end="2025-01-01", period="1d")
        hist_prices['daily_return'] = hist_prices["Close"].pct_change()
        hist_prices["volatility"] = hist_prices["daily_return"].rolling(
            window=30).std()
        latest_volatility = hist_prices["volatility"].dropna(
        ).iloc[-1] * np.sqrt(252)
        metrics['volatility'] = latest_volatility * 100
    except Exception as e:
        print(
            f"[Error] Could not calculate historical volatility for {symbol}: {e}")

    df_out = pd.DataFrame([metrics])
    csv_path = os.path.join(save_path, f"{symbol}_advanced_metrics.csv")
    df_out.to_csv(csv_path, index=False)
    print(f"[+] Saved advanced metrics for {symbol} to {csv_path}")

    return df_out


if __name__ == "__main__":
    # Example usage
    API_KEY = os.getenv("POLYGON_API_KEY")

    SYMBOLS = ["NEE", "FSLR", "ENPH", "RUN", "SEDG",
               "CSIQ", "JKS", "NXT", "DQ", "ARRY", "GE", 
               "IBDRY", "DNNGY", 'BEP', "CWEN", "ORA", 
               "IDA", "OPTT", "DRXGY", "EVA", "GPRE", "PLUG", "BE", "BLDP", 
               "ARL", "OPTT", "CEG", "VST", "CCJ", "LEU", "SMR", "OKLO", 
               "NNE", "BWXT", "BW", "NLR", "TAN", "FAN", "ICLN", "PBW", "HYDR"
               ]

    #SYMBOLS = ["VWS"]


    for symbol in SYMBOLS:
        data_yf_technical = pull_historical_data_polygon_all_time(
            symbol=symbol,
            api_key=API_KEY
        )

        # data_yf = pull_financial_data_yf(symbol)
        data_yf = pull_financial_statements(symbol)
        data_yf2 = pull_financial_overview(symbol)
        data_yf3 = pull_advanced_metrics(symbol)

