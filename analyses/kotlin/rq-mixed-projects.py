#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from common.graphs import setup_plots, save_figure
from common.local import *
from common.tables import *
from common.df import get_df
import matplotlib.ticker as mtick

summarized = load_pre_summarized('kotlin',
                                 ['project', 'location', 'isinferred'])
summarized = summarized[summarized.total > 0]

df_mixed = get_df('mixed-projects', 'kotlin', header='infer')
print(df_mixed.head())
df_mixed = df_mixed[df_mixed.java_count > 0]
print(df_mixed.head())

summarized = df_mixed.merge(summarized, on=['project'], how='left')


# %% generate the plot
fig, ax = setup_plots()

sns.boxplot(x='location',
            y='percent',
            hue='isinferred',
            hue_order=['Inferred', 'Not Inferred'],
            data=summarized,
            ax=ax,
            order=['Field', 'Global Variable', 'Lambda Arg', 'Local Variable', 'Loop Var', 'Return Type'],
            showfliers=False)

ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_ylabel('Percent per Project')
ax.set_xlabel('')
ax.get_legend().set_title('')
ax.legend(loc='upper right')

save_figure(fig, 'rq-mixed-projects.pdf', subdir='kotlin')
fig

# %% generate the table
data = summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe()
styler = highlight_cols(highlight_rows(get_styler(drop_count_if_same(drop_outer_column_index(data)))))

save_table(styler, 'rq-mixed-projects.tex', subdir='kotlin')