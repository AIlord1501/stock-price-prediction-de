# ingest.py
import yfinance as yf
import pandas as pd
from pathlib import Path
import argparse

RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")

def download_ticker(ticker: str, period="5y", interval="1d"):
    """Download OHLCV data for one ticker from Yahoo Finance."""
    df = yf.download(ticker, period=period, interval=interval)
    if df is None or df.empty:
        print(f"No data found for {ticker} (period={period}, interval={interval})")
        return None
    df.reset_index(inplace=True)  # make Date a column
    return df

def save_raw_and_parquet(df: pd.DataFrame, ticker: str):
    # Ensure directories exist
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)

    # Save raw CSV
    csv_path = RAW_DIR / f"{ticker}.csv"
    df.to_csv(csv_path, index=False)

    # Save cleaned Parquet
    parquet_path = CLEAN_DIR / f"{ticker}.parquet"
    df.to_parquet(parquet_path, engine="pyarrow", index=False)

    print(f"✅ Saved raw: {csv_path}")
    print(f"✅ Saved parquet: {parquet_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True, help="Stock ticker, e.g. AAPL")
    args = parser.parse_args()

    data = download_ticker(args.ticker)

    if data is not None and not data.empty:
        save_raw_and_parquet(data, args.ticker)
    else:
        print(f"⚠️ No data downloaded for {args.ticker}, skipping save.")






