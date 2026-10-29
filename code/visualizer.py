import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class MatrixPlotter:
    def __init__(self):
        plt.style.use('default')

    def plot_heatmap(self, data_dict: dict, title: str, plot_type: str = 'correlation'):
        df = pd.DataFrame(data_dict).T.dropna(how='all')
        
        if plot_type == 'adf':
            ordered = ['Price Return (ADF)', 'Log Volume (ADF)']
            cmap, vmin, vmax = 'RdYlGn_r', 0, 0.10
            cbar_label = 'P-Value (Green <= 0.05 is Stationary)'
        else:
            if "09:30 AM" in df.columns:
                ordered = ["09:30 AM", "10:30 AM", "11:30 AM", "12:30 PM", "01:30 PM", "02:30 PM", "03:30 PM"]
            else:
                ordered = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM"]
            cmap, vmin, vmax = 'coolwarm', None, None
            cbar_label = 'Pearson Correlation'
            
        ordered = [col for col in ordered if col in df.columns]
        df = df[ordered]
        
        fig_width = 8 if plot_type == 'adf' else 9
        plt.figure(figsize=(fig_width, max(6, len(df) * 0.35)))
        
        if plot_type == 'adf':
            sns.heatmap(df, cmap=cmap, vmin=vmin, vmax=vmax, annot=True, fmt=".4f", linewidths=0.5, annot_kws={"size": 9}, cbar_kws={'label': cbar_label})
        else:
            sns.heatmap(df, cmap=cmap, center=0, annot=True, fmt=".2f", linewidths=0.5, annot_kws={"size": 8}, cbar_kws={'label': cbar_label})
            
        plt.title(title, fontsize=14, pad=15)
        plt.xlabel('Metrics' if plot_type == 'adf' else 'Trading Window', fontsize=12)
        plt.ylabel('Stock Ticker', fontsize=12)
        plt.xticks(rotation=45 if plot_type == 'correlation' else 0)
        plt.tight_layout()
        plt.show() 
