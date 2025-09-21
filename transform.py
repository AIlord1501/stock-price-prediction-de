import pandas as pd
from pathlib import Path
import argparse


RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/clean")

def transform(ticker:str):
    raw_path = RAW_DIR / f"{ticker}.csv"
    if not raw_path.exists():
        print("raw file not found")
        return
    
    df = pd.read_csv(raw_path,parse_dates=["dates"])
    df.columns = [c.lower() for c in df.columns]
    
    df = df.ffill().dropna()

    df["close_lag1"] = df["close"].shift(1)

    # 5-day moving average
    df["close_ma5"] = df["close"].rolling(window=5).mean()

    # 10-day moving average
    df["close_ma10"] = df["close"].rolling(window=10).mean()
    
    df = df.dropna()

    CLEAN_DIR.mkdir(parents=True,exist_ok=True)
    out_path = CLEAN_DIR / f"{ticker}.parquet"
    df.to_parquet(out_path,engine="pyarrow",index=False)

    print(f"Transformed")

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker",required=True,help="stock ticker")
    args = parser.parse_args()

    transform(args.ticker)
    
    


