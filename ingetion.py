import yfinance as yf
from pathlib import Path
import argparse as arg

RAW_DIR = Path("data/raw")

""" downloads the data from the yfinance """
def download_data(ticker: str ,period = "1y",interval= "1d"):
    df = yf.download(ticker,period=period,interval=interval)
    if df is None or df.empty:
        return AttributeError
    df.reset_index(drop=True,inplace=True)
    return df
    
""" converts the data into csv"""
import pandas as pd
def save_raw(df:pd.DataFrame,ticker :str):
    RAW_DIR.mkdir(parents=True,exist_ok=True)
    outputpath = RAW_DIR / f"{ticker}.csv"
    df.to_csv(outputpath,index=False)
    print(" succes ")

if __name__ =="__main__":
    parser = arg.ArgumentParser()
    parser.add_argument("--ticker",required=True,help="stock ticker")
    args = parser.parse_args()

    data = download_data(args.ticker)

    if data is None and not data.empty:
        save_raw(data,args.ticker)
    else:
        print(" retry")
