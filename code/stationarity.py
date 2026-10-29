import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class DataStationarity:
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'Datetime' in df.columns:
            df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True).dt.tz_convert('US/Eastern')
            df = df.set_index('Datetime')
        elif not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index, utc=True).dt.tz_convert('US/Eastern')
            
        df['Log_Close_Diff'] = np.log(df['Close']).diff()
        df['Log_Vol'] = np.log(df['Volume'] + 1)
        return df.dropna()

    def run_adf_test(self, series: pd.Series) -> float:
        if len(series) > 15:
            return adfuller(series)[1]
        return np.nan
