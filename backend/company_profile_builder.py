import os
import requests
import pandas as pd
from datetime import datetime
import yfinance as yf


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


def pull_technical_data_polygon(
    symbol: str,
    api_key: str,
    start: str = "2020-01-01",
    end: str = None,
    save_path: str = "./company_profiles"
):
    """
    Fetches fundamental & technical data for a given stock symbol from the Polygon.io API
    and saves it to CSV, using manual indicator calculations (no pandas-ta).

    Returns a dictionary with 'info', 'financials', and 'tech_data'.
    """
    # Validate or set end date
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")

    os.makedirs(save_path, exist_ok=True)

    output_data = {
        "info": None,
        "financials": pd.DataFrame(),
        "tech_data": pd.DataFrame(),
    }

    ############################################################################
    # PART A: Basic Ticker Info (v3/reference/tickers/{symbol})
    ############################################################################
    info_url = f"https://api.polygon.io/v3/reference/tickers/{symbol.upper()}"
    params_info = {"apiKey": api_key}
    try:
        resp_info = requests.get(info_url, params=params_info, timeout=10)
        resp_info.raise_for_status()
        data_info = resp_info.json()

        if "results" in data_info and "ticker" in data_info["results"]:
            # Convert to Series
            ticker_data = data_info["results"]
            info_series = pd.Series(ticker_data, name="Value")
            output_data["info"] = info_series

            # Save to CSV
            df_info = pd.DataFrame(info_series, columns=["Value"])
            df_info.to_csv(f"{save_path}/{symbol}_info.csv")
        else:
            print(f"No 'ticker' field found for symbol {symbol}.")
    except Exception as e:
        print(f"Failed to fetch info for {symbol}: {e}")

    ############################################################################
    # PART B: Historical OHLC (v2/aggs)
    ############################################################################
    ohlc_url = f"https://api.polygon.io/v2/aggs/ticker/{symbol.upper()}/range/1/day/{start}/{end}"
    params_ohlc = {
        "adjusted": "true",
        "sort": "asc",
        "limit": 50000,
        "apiKey": api_key
    }
    try:
        resp_ohlc = requests.get(ohlc_url, params=params_ohlc, timeout=10)
        resp_ohlc.raise_for_status()
        data_ohlc = resp_ohlc.json()

        if data_ohlc.get("resultsCount", 0) > 0:
            bars = data_ohlc["results"]
            df_bars = pd.DataFrame(bars)

            # Rename columns: t (timestamp ms), o, h, l, c, v
            df_bars.rename(columns={
                "t": "timestamp",
                "o": "open",
                "h": "high",
                "l": "low",
                "c": "close",
                "v": "volume"
            }, inplace=True)

            df_bars["timestamp"] = pd.to_datetime(
                df_bars["timestamp"], unit="ms")
            df_bars.sort_values("timestamp", inplace=True)
            df_bars.reset_index(drop=True, inplace=True)

            # Compute manual indicators:
            # 1) SMA(50) & SMA(200)
            df_bars["SMA_50"] = compute_sma(df_bars["close"], 50)
            df_bars["SMA_200"] = compute_sma(df_bars["close"], 200)

            # 2) RSI(14)
            # We'll set index to timestamp first
            df_bars.set_index("timestamp", inplace=True)
            df_bars["RSI_14"] = compute_rsi(df_bars)
            df_bars.reset_index(inplace=True)

            # Save the final result
            df_bars.to_csv(f"{save_path}/{symbol}_technical.csv", index=False)
            output_data["tech_data"] = df_bars
        else:
            print(
                f"No historical data found for {symbol} from {start} to {end}.")
    except Exception as e:
        print(f"Failed to fetch OHLC data for {symbol}: {e}")

    return output_data


# The exact columns (and order) you want in the CSV:
CSV_COLUMNS = [
    "ticker",
    "company_name",
    "fiscal_year",
    "fiscal_period",
    "start_date",
    "end_date",
    "filing_date",
    "total_assets",
    "total_liabilities",
    "equity",
    "short_term_debt",
    "long_term_debt",
    "cash_on_hand",
    "revenues",
    "net_income",
    "ebitda",
    "net_cash_flow",
    "operating_cashflow",
    "capex",
    "fcf",
    "fcf_yield",
    "ev_ebitda",
    "p_e",
    "p_e_g",
    "debt_ebitda",
    "roic"
]


def get_most_recent_value(df: pd.DataFrame, row_label: str):
    """
    Safely extract the most recent (first column) value for a given 'row_label'
    in a yfinance DataFrame. If not found, return None.
    """
    if df.empty:
        return None
    try:
        return df.loc[row_label].iloc[0]  # First column is the most recent
    except (KeyError, IndexError):
        return None


def pull_financial_data_yf(symbol: str, save_path: str = "./company_profiles"):
    """
    Fetches quarterly data from yfinance (balance sheet, income statement, cash flow),
    along with market info (market cap, enterprise value) and computes:

      - fcf
      - fcf_yield
      - ev_ebitda
      - p_e
      - p_e_g
      - debt_ebitda
      - roic

    Saves a CSV with columns:
      ticker,company_name,fiscal_year,fiscal_period,start_date,end_date,filing_date,
      total_assets,total_liabilities,equity,short_term_debt,long_term_debt,cash_on_hand,
      revenues,net_income,ebitda,net_cash_flow,operating_cashflow,capex,fcf,fcf_yield,
      ev_ebitda,p_e,p_e_g,debt_ebitda,roic
    """

    # 1) Create output folder if needed
    os.makedirs(save_path, exist_ok=True)

    # 2) Fetch data from yfinance
    stock = yf.Ticker(symbol)

    # Use quarterly calls to approximate the "most recent quarter"
    bs = stock.quarterly_balance_sheet
    inc = stock.quarterly_financials
    cfs = stock.quarterly_cashflow
    # Contains market data (marketCap, enterpriseValue, etc.)
    info = stock.info
    print(inc)

    # 3) Prepare a dictionary for the row data with all columns = None initially
    row = {col: None for col in CSV_COLUMNS}

    # Fill the easy ones:
    row["ticker"] = symbol.upper()
    row["company_name"] = info.get("shortName", None)
    row["fiscal_year"] = None
    row["fiscal_period"] = None
    row["start_date"] = None
    row["end_date"] = None
    row["filing_date"] = None

    # ======== BALANCE SHEET ========
    row["total_assets"] = get_most_recent_value(bs, "Total Assets")
    row["total_liabilities"] = get_most_recent_value(bs, "Total Liab")
    row["equity"] = get_most_recent_value(bs, "Total Stockholder Equity")

    # short_term_debt, long_term_debt, cash_on_hand
    st_debt = get_most_recent_value(bs, "Short Long Term Debt")
    lt_debt = get_most_recent_value(bs, "Long Term Debt")
    cash_val = get_most_recent_value(bs, "Cash")

    # If any are None, treat them as 0
    row["short_term_debt"] = st_debt if st_debt is not None else 0.0
    row["long_term_debt"] = lt_debt if lt_debt is not None else 0.0
    row["cash_on_hand"] = cash_val if cash_val is not None else 0.0

    # ======== INCOME STATEMENT ========
    row["revenues"] = get_most_recent_value(inc, "Total Revenue")
    row["net_income"] = get_most_recent_value(inc, "Net Income")
    row["ebitda"] = None  # yfinance typically doesn't show direct "EBITDA" row

    # ======== CASH FLOW ========
    row["net_cash_flow"] = get_most_recent_value(cfs, "Change In Cash")
    op_cf = get_most_recent_value(cfs, "Total Cash From Operating Activities")
    capex_val = get_most_recent_value(cfs, "Capital Expenditures")
    row["operating_cashflow"] = op_cf if op_cf is not None else None
    row["capex"] = capex_val if capex_val is not None else None

    # 4) Retrieve market data from stock.info
    market_cap = info.get("marketCap", 0.0)
    enterprise_value = info.get("enterpriseValue", None)
    if not enterprise_value:  # If None or 0, we try to do a naive EV calc
        enterprise_value = market_cap + \
            (row["short_term_debt"] + row["long_term_debt"]) - row["cash_on_hand"]

    # Convert floats that might be np.nan to 0 where needed
    total_debt = (row["short_term_debt"] or 0) + (row["long_term_debt"] or 0)
    cash_on_hand_val = row["cash_on_hand"] or 0
    net_income_val = row["net_income"] or 0
    op_cf_val = row["operating_cashflow"] or 0
    capex_val = row["capex"] or 0
    eq_val = row["equity"] or 0

    # 5) Compute metrics (keeping the same logic from your snippet)

    # (a) FCF = operating_cf + capex (capex is negative)
    fcf = None
    if (op_cf_val != 0) or (capex_val != 0):
        # We'll treat missing as 0 in the sense that if either is None, we can't do math
        if pd.notna(op_cf_val) and pd.notna(capex_val):
            fcf = op_cf_val + capex_val  # if capex is negative, this is OCF + negative
    row["fcf"] = fcf

    # (b) FCF Yield = fcf / market_cap
    fcf_yield = None
    if fcf and market_cap and market_cap != 0:
        fcf_yield = fcf / market_cap
    row["fcf_yield"] = fcf_yield

    # (c) EV / EBITDA
    # since we don't have an "ebitda" row, let's see if we have 'ebitda' in info
    ebitda_info = info.get("ebitda", None)
    ev_ebitda = None
    if ebitda_info and ebitda_info != 0 and enterprise_value:
        ev_ebitda = enterprise_value / ebitda_info
    row["ev_ebitda"] = ev_ebitda

    # (d) P/E = market_cap / net_income
    p_e = None
    if net_income_val != 0 and market_cap != 0:
        p_e = market_cap / net_income_val
    row["p_e"] = p_e

    # (e) PEG
    # can't do yoy from 1 quarter; store None
    row["p_e_g"] = None

    # (f) Debt/EBITDA
    debt_ebitda = None
    if ebitda_info and ebitda_info != 0 and total_debt != 0:
        debt_ebitda = total_debt / ebitda_info
    row["debt_ebitda"] = debt_ebitda

    # (g) ROIC ~ net_income / (equity + total_debt)
    roic = None
    if (net_income_val != 0) and ((eq_val + total_debt) != 0):
        roic = net_income_val / (eq_val + total_debt)
    row["roic"] = roic

    # 6) Build a single-row DataFrame with the columns in the specified order
    df_out = pd.DataFrame(
        [[row[col] for col in CSV_COLUMNS]], columns=CSV_COLUMNS)

    # 7) Save CSV
    out_file = os.path.join(save_path, f"{symbol}_financials.csv")
    df_out.to_csv(out_file, index=False)

    # Return the DataFrame as well
    return df_out


if __name__ == "__main__":
    # Example usage
    POLYGON_API_KEY = "4cR_irLDgivxae1WO4y0Wb30VYxXRkQj"
    symbols = ["NEE", "FSLR"]

    for symbol in symbols:
        data_polygon = pull_technical_data_polygon(
            symbol=symbol,
            api_key=POLYGON_API_KEY,
            start="2022-01-01",
            end="2023-01-01"
        )

        data_yf = pull_financial_data_yf(symbol)

        print("\n=== Basic Ticker Info ===")
        print(data_polygon["info"].head(10)
              if data_polygon["info"] is not None else "None")

        print("\n=== Financials (head) ===")
        print(data_yf.head())

        print("\n=== Technical Data (tail) ===")
        print(data_polygon["tech_data"].tail())
