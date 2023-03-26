#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from common.graphs import setup_plots, save_figure
from common.local import *
from common.tables import *
from matplotlib.ticker import PercentFormatter

summarized = load_pre_summarized('kotlin',
                                 ['project', 'location', 'isval', 'isinferred'])
summarized = summarized[summarized.total > 0]
summarized = summarized[summarized['location'] != 'Return Type']
summarized = summarized[summarized['location'] != 'Lambda Arg']
summarized = summarized[summarized['location'] != 'Loop Var']
summarized = summarized[summarized['location'] != 'Global Variable']
summarized = summarized.rename(columns = {'isval': 'Is Mutable'})

# %% generate the plot
setup_plots()

figure = sns.catplot(x='location',
                     y='percent',
                     hue='isinferred',
                     hue_order=['Inferred', 'Not Inferred'],
                     col='Is Mutable',
                     data=summarized,
                     order=['Field', 'Local Variable'],
                     sharey=True,
                     showfliers=False,
                     kind='box')
figure.set_axis_labels('', 'Percent per Project')
figure.legend.set_title('')
for ax in figure.axes.flat:
    ax.yaxis.set_major_formatter(PercentFormatter())

save_figure(figure.figure, 'rq-mutability-summary.pdf', subdir='kotlin')
figure.figure

summarized['Is Mutable'] = summarized['Is Mutable'].apply(lambda x: 'Mutable' if x else 'Not Mutable')

# %% generate the table
data = summarized[['location', 'isinferred', 'Is Mutable', 'percent']] \
    .groupby(['location', 'isinferred', 'Is Mutable']) \
    .describe()
styler = highlight_rows(highlight_cols(get_styler(drop_count_if_same(drop_outer_column_index(data).rename(columns={'count': 'projects'})))))

save_table(styler, 'rq-mutability-summary.tex', subdir='kotlin')

# %%
