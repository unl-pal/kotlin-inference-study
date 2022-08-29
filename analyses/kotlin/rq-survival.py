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

from lifelines import KaplanMeierFitter
from matplotlib import pyplot as plt

print('Loading survival data', flush=True)
df = get_deduped_df('survival', 'kotlin', header='infer')
print('Survival data loaded', flush=True)

bad_projects = df[df['timetochange'] < 0]['project'].unique()
df = df[~df['project'].isin(bad_projects)]

# %% generate the table
print('Summarizing Time to Change by Change Kind')
df_summarized = df.groupby(['changekind'])[['timetochange']] \
    .describe() \
    .transpose()
summarized_styler = highlight_cols(highlight_rows(get_styler(df_summarized)))
save_table(summarized_styler, 'time-to-change-by-changetype.tex', subdir='kotlin')

# %% generate the plot
print('Fitting Survival Curves')
fitter = KaplanMeierFitter()
fig, ax = setup_plots()

starts_inferred = df['startinferred']

T = df['timetochange']
E = df['observed']

print('Fitting starting inferred')
fitter.fit(T[starts_inferred], E[starts_inferred], label='Starts Inferred')
fitter.plot_survival_function(ax=ax)

print('Fitting starting annotated')
fitter.fit(T[~starts_inferred], E[~starts_inferred], label='Starts Annotated')
fitter.plot_survival_function(ax=ax)

plt.title('Lifespans of items')
save_figure(fig, 'lifespans.pdf', subdir='kotlin')
fig

# %%
