#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from common.graphs import setup_plots, save_figure
from common.local import *
from common.tables import *
from common.df import get_df
import matplotlib.ticker as mtick

# %%

df_file_counts = get_df('basic-usage', 'kotlin', header='infer') \
    .query("file != 'DUMMYDUMMYDUMMY.kt'") \
    [['project', 'file']] \
    .groupby('project', as_index=False) \
    .count() \
    .rename(columns={'file': 'kotlin_count'})

# %%

summarized = load_pre_summarized('kotlin',
                                 ['project', 'location', 'isinferred'])
summarized = summarized[summarized.total > 0]

# %%
df_mixed = get_df('mixed-projects', 'kotlin', header='infer')

mixed_count = len(df_mixed.loc[df_mixed.java_count > 0])
total_count = len(df_mixed)

print("%.2f%% of projects are mixed" % (100 * (mixed_count / total_count)))

df_mixed = df_mixed[df_mixed.java_count > 0]

df_mixed_percent = pd.merge(df_mixed, df_file_counts, on='project') \
    .assign(file_count = lambda d: d.java_count.add(d.kotlin_count),
            percent_java = lambda d: d.java_count.div(d.file_count).mul(100).round(3))

# %%

summarized = df_mixed.merge(summarized, on=['project'], how='left')

# %% generate the plot
fig, ax = setup_plots()

sns.boxplot(x='location',
            y='percent',
            hue='isinferred',
            hue_order=['Inferred', 'Not Inferred'],
            data=summarized,
            ax=ax,
            order=location_order,
            showfliers=False)

ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_ylabel('Percent per Project')
ax.set_xlabel('')
ax.get_legend().set_title('')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
save_figure(fig, 'rq-mixed-projects.pdf', subdir='kotlin')
fig

# %% generate the table
data = summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe()
styler = highlight_cols(highlight_rows(get_styler(drop_count_if_same(drop_outer_column_index(data)))))

save_table(styler, 'rq-mixed-projects.tex', subdir='kotlin')

# %% Generate an additional table

data = df_mixed_percent[['percent_java']].rename(columns={'percent_java': '% Java'}).describe()
styler = highlight_cols(highlight_rows(get_styler(data)))

save_table(styler, 'mixed-projects-distribution.tex', subdir='kotlin')
