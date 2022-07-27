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

# print(df.head(), flush=True)
# print(df.describe(), flush=True)

fitter = KaplanMeierFitter()
ax = plt.subplot(111)

starts_inferred = df['startinferred']

T = df['timetochange']
E = df['observed']

fitter.fit(T[starts_inferred], E[starts_inferred], label='Starts Inferred')
fitter.plot_survival_function(ax=ax)

fitter.fit(T[~starts_inferred], E[~starts_inferred], label='Starts Annotated')
fitter.plot_survival_function(ax=ax)

plt.title('Lifespans of items')

save_figure(plt.gcf(), "figures/lifespans.pdf", x=7, y=4)

fitter.print_summary()
