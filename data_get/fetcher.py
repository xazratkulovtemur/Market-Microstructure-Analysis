import yfinance as yf
import os
import pandas as pd
from typing import List

class MarketDataFetcher:
    def __init__(self, base_dir: str = r"C:\Users\Xazratkulov Temur\Desktop\Market_Microstructure_Repo\data"):
        self.base_dir = os.path.abspath(base_dir)
        self.dir_5min = os.path.join(self.base_dir, "5min_2month")
        self.dir_1hour = os.path.join(self.base_dir, "1hour_1year")
        os.makedirs(self.dir_5min, exist_ok=True)
        os.makedirs(self.dir_1hour, exist_ok=True)

    def fetch_and_save(self, tickers: List[str], interval: str):
        if interval == '5m':
            period, save_dir, suffix = "60d", self.dir_5min, "5m_data"
        elif interval == '1h':
            period, save_dir, suffix = "1y", self.dir_1hour, "1h_data"
        else:
            raise ValueError("Interval must be '5m' or '1h'.")

        print(f"\nStarting batch download: {period} period at {interval} intervals...")
        for ticker_symbol in tickers:
            try:
                ticker = yf.Ticker(ticker_symbol)
                data = ticker.history(period=period, interval=interval)
                if data.empty:
                    continue
                file_path = os.path.join(save_dir, f"{ticker_symbol}_{suffix}.csv")
                data.to_csv(file_path)
                print(f"  -> Saved: {file_path}")
            except Exception as e:
                print(f"  -> Error {ticker_symbol}: {e}")
