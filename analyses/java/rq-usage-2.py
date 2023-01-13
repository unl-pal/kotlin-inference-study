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

summarized = load_pre_summarized('java',
                                 ['project', 'location', 'isinferred'])

summarized_sum = summarized.groupby(['project'])[['count']].sum().rename(columns={'count': 'total'})
summarized = summarized.drop(columns={'total'}).merge(summarized_sum, on=['project'], how='left')
summarized['percent'] = summarized.apply(
    lambda x: 0 if x['total'] == 0 else (x['count'] / x['total']) * 100,
    axis=1)

# %% generate the plot
fig, ax = setup_plots()
sns.boxplot(x='location',
            y='percent',
            hue='isinferred',
            data=summarized,
            ax=ax,
            order=['Field', 'Global Variable', 'Lambda Arg', 'Local Variable', 'Loop Var', 'Return Type'],
            showfliers=False)

ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.set_ylabel('Percent per Project')
ax.set_xlabel('')
ax.get_legend().set_title('')

save_figure(fig, 'rq-usage-summary-2.pdf', subdir='java', x=2.3)
fig

# %% generate the table
data = summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe()
styler = highlight_cols(highlight_rows(get_styler(drop_count_if_same(drop_outer_column_index(data)))))

save_table(styler, 'rq-usage-summary-2.tex', subdir='java')
