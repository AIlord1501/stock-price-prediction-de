import pandas as pd
import pathlib
import argparse

RAW_DIR = pathlib.Path("data/raw")
CLEAN_DIR = pathlib.Path("data/clean")


def transform(ticker:str):
    rawpath  = RAW_DIR / f"{ticker}.csv"
    if not rawpath.exists():
        print(" didnt find the file")
        return
    df = pd.read_csv(rawpath,parse_dates=["dates"])
    
    """ some transformations to the data"""
    df.columns = [c.lower() for c in df.columns]
    df = df.ffill().dropna()

    df["return"] = df["close"].pct_change()
    df["target"] = df["return"].shift(-1)

    df["lag1"] = df["return"].shift(1)
    df["lag5"] = df["return"].rolling(5).mean()
    df["vol"] = df["return"].rolling(5).std()

    CLEAN_DIR.mkdir(parents=True,exist_ok=True)
    out_path = CLEAN_DIR / f"{ticker}.csv"

    print(f"transformed")

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker",required=True,help="stock ticker")
    args = parser.parse_args()

    transform(args.ticker)
