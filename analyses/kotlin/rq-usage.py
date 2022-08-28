#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from common.graphs import setup_plots, save_figure
from common.local import *
from common.tables import *
import matplotlib.ticker as mtick

summarized = load_pre_summarized('kotlin',
                                 ['project', 'location', 'isinferred'])

# %% generate the plot
fig, ax = setup_plots()

sns.boxplot(x='location',
            y='percent',
            hue='isinferred',
            data=summarized,
            ax=ax,
            showfliers=False)

ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_ylabel('Percent per Project')
ax.set_xlabel('')
fig.legend().set_title('')

save_figure(fig, 'rq-usage-summary.pdf', subdir='kotlin')
fig

# %% generate the table
data = summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe()
styler = highlight_cols(highlight_rows(get_styler(data)))

save_table(styler, 'rq-usage-summary.tex', subdir='kotlin')

# %%