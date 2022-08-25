#!/usr/bin/env python
# coding: utf-8

from common.local import *
from common.tables import *
from common.df import *

from matplotlib import pyplot as plt
import seaborn as sns

from lifelines import KaplanMeierFitter

set_style()

print("Loading survival data", flush=True)
df = get_df("survival", "kotlin", header='infer')
print("Survival data loaded", flush=True)

print("Summarizing Time to Change by Change Kind")
df_summarized = df.groupby(['changekind'])[['timetochange']].describe().transpose()
summarized_styler = highlight_cols(highlight_rows(get_styler(df_summarized)))
save_table(summarized_styler, "time-to-change-by-changetype.tex", "rq-survival")

print("Fitting Survival Curves")
fitter = KaplanMeierFitter()
ax = plt.subplot(111)

starts_inferred = df['startinferred']

T = df['timetochange']
E = df['observed']

print("Fitting starting inferred")
fitter.fit(T[starts_inferred], E[starts_inferred], label='Starts Inferred')
fitter.plot_survival_function(ax=ax)

print("Fitting starting annotated")
fitter.fit(T[~starts_inferred], E[~starts_inferred], label='Starts Annotated')
fitter.plot_survival_function(ax=ax)

plt.title('Lifespans of items')
save_figure(plt.gcf(), "lifespans.pdf", x=7, y=4)
