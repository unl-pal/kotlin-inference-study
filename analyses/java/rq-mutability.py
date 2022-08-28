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

summarized = load_pre_summarized('java',
                                 ['project', 'location', 'isval', 'isinferred'])
summarized = summarized[summarized['location'] != 'Return Type']
summarized = summarized[summarized['location'] != 'Lambda Args']
summarized = summarized[summarized['location'] != 'Loop Var']

# %% generate the plot
setup_plots()

figure = sns.catplot(x='location',
                     y='percent',
                     hue='isinferred',
                     col='isval',
                     data=summarized,
                     sharey=True,
                     showfliers=False,
                     kind='box')
figure.set_axis_labels('', 'Percent per Project')
figure.legend.set_title('')
for ax in figure.axes.flat:
    ax.yaxis.set_major_formatter(PercentFormatter())

save_figure(figure.figure, 'rq-mutability-summary.pdf', subdir='java')
figure.figure

# %% generate the table
data = summarized[['location', 'isinferred', 'isval', 'percent']] \
    .groupby(['location', 'isinferred', 'isval']) \
    .describe()
styler = highlight_rows(highlight_cols(get_styler(data)))

save_table(styler, 'rq-mutability-summary.tex', subdir='java')

# %%