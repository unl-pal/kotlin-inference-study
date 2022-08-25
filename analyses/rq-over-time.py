#!/usr/bin/env python
# coding: utf-8

from common.local import *
from common.tables import *
from common.df import *
import pandas as pd
from matplotlib.ticker import PercentFormatter

def get_time_data():
    path_to_parquet = "data/parquet/kotlin/over-time-processed.parquet"
    try:
        df = pd.read_parquet(path_to_parquet)
    except:
        df = get_df("over-time", "kotlin", header='infer')
        df['time'] = pd.to_datetime(df['time'], unit='us', origin='unix')
        df.to_parquet(path_to_parquet, compression = 'gzip')
    return df

set_style()

pd.set_option('display.max_columns', None)
df = get_time_data()
print(df.head())

fig, ax = plt.subplots(1, 1)
plt.figure()
sns.lineplot(x='time', y='count', style='isinferred', hue='location', data=df, ax=ax, err_style='band', sort=True)
save_figure(fig, "rq-over-time-summary.pdf", 7, 4)
