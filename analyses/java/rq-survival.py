#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from common.graphs import setup_plots, save_figure
from common.local import *
from common.tables import *
from common.df import *

import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from matplotlib import pyplot as plt

print('Loading survival data', flush=True)
df = get_deduped_df('survival', 'java', header='infer')
print('Survival data loaded', flush=True)

print('Converting to duration...', flush=True)
df['timetochange'] = pd.to_timedelta(df['timetochange'], unit='us')
print('Converted to duration.', flush=True)

bad_projects = df[df['timetochange'] < np.timedelta64(0, 's')]['project'].unique()
df = df[~df['project'].isin(bad_projects)]

# %% generate the table
print('Summarizing Time to Change by Change Kind')
df_summarized = df.groupby(['changekind'])[['timetochange']] \
    .describe() \
    .transpose()
summarized_styler = highlight_cols(highlight_rows(get_styler(df_summarized)))
save_table(summarized_styler, 'time-to-change-by-changetype.tex', 'java')

# %% generate the plot
print('Fitting Survival Curves')
fitter = KaplanMeierFitter()
fig, ax = setup_plots()

df['timetochange'] = df['timetochange'].apply(lambda x: x.days)

starts_inferred = df['startinferred']
after_jdk10 = df['afterjdk10']


T = df['timetochange']
E = df['observed']

print('Fitting starting annotated (before JDK10)')
fitter.fit(T[~starts_inferred & ~after_jdk10], E[~starts_inferred & ~after_jdk10], label='Starts Not Inferred (pre-JDK10)')
fitter.plot_survival_function(ax=ax)

print('Fitting starting inferred')
fitter.fit(T[starts_inferred], E[starts_inferred], label='Starts Inferred')
fitter.plot_survival_function(ax=ax)

print('Fitting starting annotated (after JDK10)')
fitter.fit(T[~starts_inferred & after_jdk10], E[~starts_inferred & after_jdk10], label='Starts Not Inferred (post-JDK10)')
fitter.plot_survival_function(ax=ax)

ax.set_ylabel('Estimated probability of staying in state ($\hat{S}(t)$)')
ax.set_xlabel('time $t$ (days)')
ax.set_xscale('log')

# plt.title('Lifespans of items')
save_figure(fig, 'lifespans.pdf', subdir='java')
fig

# %%
