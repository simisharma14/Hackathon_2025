import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def convert_iso_to_mm_dd_yyyy(iso_str: str) -> str:
    """
    Convert an ISO or YYYY-MM-DD date string (e.g. '2024-06-28' or '2024-06-28T15:43:00Z')
    to 'MM-DD-YYYY'. If parsing fails, return the original string.
    """
    if not isinstance(iso_str, str):
        return iso_str
    possible_formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d"
    ]
    for fmt in possible_formats:
        try:
            dt = datetime.strptime(iso_str, fmt)
            return dt.strftime("%m-%d-%Y")
        except ValueError:
            pass
    # If none of the formats worked, just return the original
    return iso_str

def get_federal_register_docs(symbol: str, per_page: int = 20, max_pages: int = 3) -> pd.DataFrame:
    base_url = "https://www.federalregister.gov/api/v1/articles"
    # We'll filter by the last 30 days, similar to your approach
    today = datetime.now()
    cutoff_date = today - timedelta(days=30)

    results = []

    # We'll fetch up to max_pages
    for page_num in range(1, max_pages + 1):
        params = {
            "conditions[term]": symbol,   # Searching the symbol as a keyword
            "order": "newest",
            "per_page": per_page,  # up to 100
            "page": page_num
        }
        resp = requests.get(base_url, params=params)
        if resp.status_code != 200:
            print(f"Error fetching page {page_num} for {symbol}. HTTP {resp.status_code}")
            break

        data = resp.json()
        articles = data.get("results", [])
        if not articles:
            # No more results
            break

        # Parse each article
        for item in articles:
            pub_date_iso = item.get("publication_date", "")  # Usually 'YYYY-MM-DD'
            pub_date_str = convert_iso_to_mm_dd_yyyy(pub_date_iso)

            # Convert back to datetime for filtering
            try:
                pub_dt = datetime.strptime(pub_date_str, "%m-%d-%Y")
            except ValueError:
                # If date parsing fails, skip
                continue

            if pub_dt < cutoff_date:
                # The item is older than 30 days, skip
                continue

            title = item.get("title", "No Title")
            url = item.get("html_url", "No URL")
            # 'source' is not really a Federal Register concept. We'll treat 'agency_names' as source.
            agencies = item.get("agencies", [])
            # agencies might be a list of dicts, e.g. [{'name': 'Securities and Exchange Commission'}]
            if agencies and isinstance(agencies, list):
                agency_names = [a.get("name", "") for a in agencies]
                source_str = "; ".join(agency_names) if agency_names else "Unknown"
            else:
                source_str = "Unknown"

            # Append to our results
            results.append({
                "timestamp": pub_date_str,
                "title": title,
                "url": url,
                "source": source_str
            })

    return pd.DataFrame(results)


if __name__ == "__main__":
    '''
    SYMBOLS = [
        "NEE", "FSLR", "ENPH", "RUN", "SEDG",
        "CSIQ", "JKS", "NXT", "SPWR", "DQ", "ARRY", "NEP", 
        "GE", "VWS", "IBDRY", "DNNGY", "BEP", "NPI", "CWEN", 
        "INOXWIND", "ORA", "IDA", "OPTT", "DRXGY", "EVA", "GPRE", 
        "PLUG", "BE", "BLDP", "ARL", "OPTT", "CEG", "VST", "CCJ", 
        "LEU", "SMR", "OKLO", "NNE", "BWXT", "BW", "TLNE"
    ]
    '''
    SYMBOLS = ["clean energy", "renewable energy", "energy efficiency", "nuclear energy", "nuclear regulation", "solar energy", "solar power", "wind power", "wind energy", "hydropower", "geothermal", "climate change"]

    # Create folder for federal register data
    save_dir = "./data/regulatory_data"
    os.makedirs(save_dir, exist_ok=True)

    for symbol in SYMBOLS:
        print(f"Fetching Federal Register documents referencing {symbol} ...")
        df_fr = get_federal_register_docs(symbol, per_page=20, max_pages=5)

        if not df_fr.empty:
            # Convert 'timestamp' to mm-dd-yyyy just to be consistent
            df_fr["timestamp"] = df_fr["timestamp"].apply(convert_iso_to_mm_dd_yyyy)

            out_path = os.path.join(save_dir, f"{symbol}_federal_register.csv")
            df_fr.to_csv(out_path, index=False)
            print(f"Saved {len(df_fr)} articles to {out_path}\n")
        else:
            print(f"No Federal Register results found for {symbol} in the last 30 days.\n")
