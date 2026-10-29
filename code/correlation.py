import pandas as pd
import numpy as np
from scipy.stats import pearsonr

class MicrostructureAnalyzer:
    def __init__(self):
        self.valid_blocks_1h = ["09:30 AM", "10:30 AM", "11:30 AM", "12:30 PM", "01:30 PM", "02:30 PM", "03:30 PM"]

    def analyze(self, df: pd.DataFrame, interval: str):
        correlations, p_values = {}, {}
        
        if interval == '1h':
            df['Time_Block'] = df.index.strftime('%I:%M %p')
            df_filtered = df[df['Time_Block'].isin(self.valid_blocks_1h)]
            for block in self.valid_blocks_1h:
                block_data = df_filtered[df_filtered['Time_Block'] == block]
                if len(block_data) > 2:
                    r, p = pearsonr(block_data['Log_Vol'], block_data['Log_Close_Diff'])
                    correlations[block], p_values[block] = r, p
                else:
                    correlations[block], p_values[block] = np.nan, np.nan
                    
        elif interval == '5m':
            df['Hour'] = df.index.hour
            df_filtered = df[df['Hour'].between(9, 16)] 
            for hour, group in df_filtered.groupby('Hour'):
                label = f"{hour if hour <= 12 else hour-12}:00 {'AM' if hour < 12 else 'PM'}"
                if len(group) > 2:
                    r, p = pearsonr(group['Log_Vol'], group['Log_Close_Diff'])
                    correlations[label], p_values[label] = r, p
                else:
                    correlations[label], p_values[label] = np.nan, np.nan

        return correlations, p_values
