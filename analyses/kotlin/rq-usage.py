#!/usr/bin/env python
# coding: utf-8

# %% Import tools
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from common.graphs import setup_plots, save_figure
from common.local import *
from common.tables import *
import matplotlib.ticker as mtick

import statsmodels.api as sm
import statsmodels.graphics as smg
import statsmodels.formula.api as smf
import statsmodels.stats as sms
import scipy.stats as stats

# %% Load Data

summarized = load_pre_summarized('kotlin',
                                 ['project', 'location', 'isinferred'])
summarized = summarized[summarized.total > 0]

# %% Build model

summarized_temp = summarized.assign(location = lambda df: df.location.str.replace('\n', ' '))

model = smf.ols('center(percent) ~ C(isinferred)*C(location) - 1', data=summarized_temp).fit()

# %% Show the model and print

print(model.summary())

sms.anova.anova_lm(model, typ=3).convert_dtypes()

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

save_figure(fig, 'rq-usage-summary.pdf', subdir='kotlin')
fig

# %% generate the table
data = summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe()
styler = highlight_cols(highlight_rows(get_styler(drop_count_if_same(drop_outer_column_index(data)))))

save_table(styler, 'rq-usage-summary.tex', subdir='kotlin')
