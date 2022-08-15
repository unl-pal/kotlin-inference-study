#!/usr/bin/env python
#coding: utf-8
import numpy as np
import pandas as pd
from common.tables import *
from common.df import *
from common.local import *
from common.tables import *
from matplotlib.ticker import PercentFormatter
from scipy.stats import shapiro
pd.set_option('display.max_colwidth', None)

df = get_df("determine-rhs-expression-types", "kotlin", header='infer')
print(df.describe())

set_style()
summarized = load_pre_summarized('kotlin', ['project', 'isinferred', 'expkind'])
plt.figure()
fig, ax = plt.subplots(1,1)
sns.boxplot(x='expkind', y='percent', hue='isinferred', data=df, ax = ax, showfliers = False)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_ylabel("Percent per Project")
ax.set_xlabel("")
plt.gca().legend().set_title("")
save_figure(fig, "figures/rq-rhs-types-summary.pdf", 7, 4)