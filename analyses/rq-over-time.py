#!/usr/bin/env python
# coding: utf-8

#%% build the dataframe
from common.graphs import setup_plots, save_figure
from common.local import *
from common.tables import *
from common.df import *
import pandas as pd
from matplotlib.ticker import PercentFormatter

def set_time_data(df):
    df['time'] = pd.to_datetime(df['time'], unit='us', origin='unix')
    return df

pd.set_option('display.max_columns', None)
df = get_df('over-time', 'kotlin', header='infer', precache_function=set_time_data)
print(df.head())

#%% generate the plot
fig, ax = setup_plots()

sns.lineplot(x='time',
             y='count',
             style='isinferred',
             hue='location',
             data=df,
             ax=ax,
             err_style='band',
             sort=True)

save_figure(fig, 'rq-over-time-summary.pdf')
fig

#%%
