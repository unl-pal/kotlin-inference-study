#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from common.tables import *
from common.graphs import setup_plots, save_figure
from common.df import *

import pandas as pd
import numpy as np
import seaborn as sns

from scipy.stats import pearsonr

df_size = pd.pivot_table(get_df('project-size', 'kotlin', header='infer'),
                         index='project', columns='count_type', values='count')

df_stars = get_df('stars', 'kotlin', header='infer')
df_num_devs = get_df('developer-count', 'kotlin', header='infer')

df_usage = get_deduped_df('basic-usage', 'kotlin', header='infer')

total_declarations = df_usage.groupby('project')['count'].sum()
inferred_declarations = df_usage[df_usage.isinferred].groupby('project')['count'].sum()
percent_annotated = inferred_declarations.div(total_declarations).mul(100).reset_index().rename(columns={'count': 'percent_annotated'})

df = pd.merge(df_size, df_stars, on='project', how='inner')
df = pd.merge(df, df_num_devs, on='project', how='inner')
df = pd.merge(df, percent_annotated, on='project', how='inner')

df = df.dropna()

for factor in ['files', 'statements', 'stars', 'developers']:
    fig, ax = setup_plots()
    sns.regplot(y='percent_annotated',
                x=factor,
                data=df,
                ci=None,
                truncate=True,
                fit_reg=True)
    r, p = pearsonr(df['percent_annotated'],
                    df[factor])
    ax.set_title(f'Correlation between Percent Inferred and {factor}\n$r = {r}$ ($p = {p}$)')
    save_figure(fig, f'correlation-{factor}.png', 6, 6, 'kotlin')
