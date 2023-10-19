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
summarized = summarized[summarized['location'] != 'Return\nType']
summarized = summarized[summarized['location'] != 'Lambda\nArgument']
summarized = summarized[summarized['location'] != 'Loop\nVariable']
# summarized = summarized[summarized['location'] != 'Global Variable']
summarized = summarized.rename(columns = {'isval': 'Is Mutable'})

# %% generate the plot

# figure = sns.catplot(x='location',
#                      y='percent',
#                      hue='isinferred',
#                      hue_order=['Inferred', 'Not Inferred'],
#                      col='Is Mutable',
#                      data=summarized,
#                      order=['Field', 'Local Variable'],
#                      sharey=True,
#                      showfliers=False,
#                      kind='box')
# figure.set_axis_labels('', 'Percent per Project')
# figure.legend.set_title('')
# for ax in figure.axes.flat:
#     ax.yaxis.set_major_formatter(PercentFormatter())

# save_figure(figure.figure, 'rq-mutability-summary.pdf', subdir='kotlin')
# figure.figure

fig, ax = setup_plots()
sns.boxplot(x='location',
            y='percent',
            hue='isinferred',
            ax=ax,
            hue_order=['Inferred', 'Not Inferred'],
            width=0.6,
            order=['Field', 'Global\nVariable', 'Local\nVariable'],
            data=summarized[summarized['Is Mutable']],
            showfliers=False)
ax.set_ylabel('Percent per Project')
ax.set_xlabel('')
ax.get_legend().set_title('')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
ax.yaxis.set_major_formatter(PercentFormatter())

save_figure(fig, 'rq-mutability-mutable.pdf', subdir='kotlin')

fig, ax = setup_plots()
sns.boxplot(x='location',
            y='percent',
            hue='isinferred',
            ax=ax,
            hue_order=['Inferred', 'Not Inferred'],
            width=0.6,
            order=['Field', 'Global\nVariable', 'Local\nVariable'],
            data=summarized[~summarized['Is Mutable']],
            showfliers=False)
ax.set_ylabel('Percent per Project')
ax.set_xlabel('')
ax.get_legend().set_title('')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
ax.yaxis.set_major_formatter(PercentFormatter())

save_figure(fig, 'rq-mutability-immutable.pdf', subdir='kotlin')

summarized['Is Mutable'] = summarized['Is Mutable'].apply(lambda x: 'Mutable' if x else 'Not Mutable')

# %% generate the table
data = summarized[['location', 'isinferred', 'Is Mutable', 'percent']] \
    .groupby(['location', 'isinferred', 'Is Mutable']) \
    .describe()
styler = highlight_rows(highlight_cols(get_styler(drop_count_if_same(drop_outer_column_index(data)))))

save_table(styler, 'rq-mutability-summary.tex', subdir='kotlin')

# %%
