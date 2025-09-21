# ingest.py
import yfinance as yf
import pandas as pd
from pathlib import Path
import argparse

RAW_DIR = Path("data/raw")

def download_ticker(ticker: str, period="5y", interval="1d"):
    """Download OHLCV data for one ticker from Yahoo Finance."""
    df = yf.download(ticker, period=period, interval=interval)
    if df is None or df.empty:
        print(f"No data found for {ticker} (period={period}, interval={interval})")
        return None
    df.reset_index(inplace=True)  # make Date a column
    return df

def save_raw(df: pd.DataFrame, ticker: str):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RAW_DIR / f"{ticker}.csv"
    df.to_csv(out_path, index=False)
    print(f"✅ Saved raw data: {out_path}")


    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True, help="Stock ticker, e.g. AAPL")
    args = parser.parse_args()

    data = download_ticker(args.ticker)

    if data is not None and not data.empty:
        save_raw(data, args.ticker)
        
    else:
        print(f"⚠️ No data downloaded for {args.ticker}, skipping save.")





