import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


CLEAN_DIR = Path("data/clean")

def run_model(ticker:str):

    #load cleaned data

    clean_path = CLEAN_DIR / f"{ticker}.csv"
    if not clean_path.exists():
        raise FileNotFoundError
    
    df = pd.read_csv(clean_path)
    df.copy()


    #feature engineering 
    df["return"] = df["close"].pct_change()
    df["target"]  = df["return"].shift(-1)

    df["lag1"] = df["return"].shift(1)
    df["lag5"] = df["return"].rolling(5).mean()
    df["vol"] = df["return"].rolling(5).std()

    df = df.dropna().reset_index(drop=True)

    features = ["lag1","lag5","vol"]

   #train/test split

    split = int(0.8 * len(df))
    train, test = df.iloc[:split], df.iloc[split:]

    X_train, y_train = train[features], train["target"]
    X_test, y_test = test[features], test["target"]


  #train model

    model = LinearRegression()
    model.fit(X_train, y_train)

# pred

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
  

    
    print(f"  MSE: {mse:.6f}")
    print(f"  R² : {r2:.4f}")
    


    test = test.copy()
    test["pred"] = y_pred
    test["signal"] = np.where(test["pred"]>0,1,0)
    test["strategy"] = test["signal"]*test["return"]

    test["cumulative_strategy"] = (1 + test["strategy"]).cumprod()
    test["cumulative_buy_hold"] = (1 + test["return"]).cumprod()

    plt.plot(test.index, test["cumulative_strategy"], label="ML Strategy")
    plt.plot(test.index, test["cumulative_buy_hold"], label="Buy & Hold")
    plt.title(f"{ticker} Strategy vs Buy & Hold")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", required=True, help="Stock ticker, e.g. AAPL")
    args = parser.parse_args()

    run_model(args.ticker)