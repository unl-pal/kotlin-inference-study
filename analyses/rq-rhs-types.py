# !/usr/bin/env python
#coding: utf-8
from unicodedata import name
import numpy as np
import pandas as pd
from common.tables import *
from common.df import *
from common.local import *
from matplotlib.ticker import PercentFormatter
from scipy.stats import shapiro
pd.set_option('display.max_colwidth', None)

df = get_df("determine-rhs-expression-types", "kotlin", header='infer')

set_style()
df_count = df[df.isinferred == True].drop(columns=['filepath','class','count'])
df_count['expkind'] = df_count.apply(lambda x: 'LITERAL' if x['expkind'] == 'LITERAL' else ('NEW' if x['expkind'] == 'NEW' else 'OTHER'), axis = 1)
df_count = df_count.groupby(['project', 'isinferred', 'expkind'])['expkind'].count().reset_index(name='count')
sum = df_count['count'].sum()
df_count['percent'] = df_count.apply(lambda x: 0 if x['count'] == 0 else (x['count'] / sum) * 100, axis = 1)
print(df_count)
print(df_count['expkind'].describe())

plt.figure()
fig, ax = plt.subplots(1,1)
sns.boxplot(x='expkind', y='percent', data=df_count, ax = ax, showfliers = False)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_ylabel("Percent per Project")
ax.set_xlabel("")
plt.xticks(rotation=90)
plt.gca().legend().set_title("")

# fig = figure.get_figure()
plt.tight_layout()
fig.set(figwidth = 7)
fig.set(figheight = 4)
fig.savefig("rq-rhs-types-summary.pdf", dpi=600)
plt.close(fig)
# save_figure(fig, "figures/rq-rhs-types-summary.pdf", 7, 4)