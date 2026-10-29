import os
import glob
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from data_get.fetcher import MarketDataFetcher
from code.stationarity import DataStationarity
from code.correlation import MicrostructureAnalyzer
from code.visualizer import MatrixPlotter

def main():
    tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK.B", "LLY", "AVGO", "JPM", "V", "WMT", "JNJ", "XOM"]

    fetcher = MarketDataFetcher()
    stationarity_engine = DataStationarity()
    analyzer = MicrostructureAnalyzer()
    plotter = MatrixPlotter()
    
    for interval in ['1h', '5m']:
        print(f"\n{'='*50}\nRUNNING PIPELINE FOR INTERVAL: {interval}\n{'='*50}")
        
        # NOTE: Fetching is ENABLED so your data rebuilds automatically
        #fetcher.fetch_and_save(tickers, interval=interval)
        
        data_folder = f"C:\\Users\\Xazratkulov Temur\\Desktop\\Market_Microstructure_Repo\\data\\1hour_1year" if interval == '1h' else f"C:\\Users\\Xazratkulov Temur\\Desktop\\Market_Microstructure_Repo\\data\\5min_2month"
        csv_files = glob.glob(os.path.join(os.path.abspath(data_folder), "*.csv"))
        
        if not csv_files:
            continue
            
        portfolio_adf, portfolio_corrs = {}, {}
        
        for file in csv_files:
            ticker = os.path.basename(file).split('_')[0]
            df = pd.read_csv(file)
            if df.empty or 'Datetime' not in df.columns: continue
                
            clean_df = stationarity_engine.transform_data(df)
            
            price_adf = stationarity_engine.run_adf_test(clean_df['Log_Close_Diff'])
            vol_adf = stationarity_engine.run_adf_test(clean_df['Log_Vol'])
            portfolio_adf[ticker] = {'Price Return (ADF)': price_adf, 'Log Volume (ADF)': vol_adf}
            
            corrs, _ = analyzer.analyze(clean_df, interval=interval)
            portfolio_corrs[ticker] = corrs
            
        print(f"\n-> Displaying ADF Stationarity Matrix ({interval})")
        plotter.plot_heatmap(portfolio_adf, title=f"ADF Test P-Values ({interval})", plot_type='adf')
        
        print(f"\n-> Displaying Correlation Matrix ({interval})")
        plotter.plot_heatmap(portfolio_corrs, title=f"Volume-Price Correlation ({interval})", plot_type='correlation')

if __name__ == "__main__":
    main()
