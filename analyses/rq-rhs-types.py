#!/usr/bin/env python
#coding: utf-8

#%% build the dataframe
import pandas as pd
from common.tables import *
from common.df import *
from common.local import *
pd.set_option('display.max_colwidth', None)

df = get_df('determine-rhs-expression-types', 'kotlin', header='infer')

def groupKinds(x):
    kind = x['expkind']
    keep = ['ARRAYACCESS', 'CAST', 'LITERAL', 'METHODCALL', 'NEW', 'STATEMENT', 'VARACCESS']
    if kind in keep:
        return kind
    if kind == 'TEMPLATE':
        return 'LITERAL'
    if kind == '??':
        return 'OTHER'
    if kind.startswith('OP_') or kind.startswith('BIT_') or kind.startswith('LOGICAL_'):
        return 'EXPRESSION'
    keep = ['EQ', 'LTEQ', 'GTEQ', 'NEQ', 'GT', 'LT', 'PAREN', 'IN']
    if kind in keep:
        return 'EXPRESSION'
    return kind

df_inferred = df[df.isinferred == True].drop(columns=['isinferred', 'filepath', 'class'])
df_inferred['expkind'] = df_inferred.apply(groupKinds, axis=1)
df_inferred = df_inferred.groupby(['project', 'expkind'])['expkind'] \
    .count() \
    .reset_index(name='count')

sums = df_inferred.groupby(['project']) \
    .sum()
df_inferred['percent'] = df_inferred.apply(lambda x: x['count'] / sums.loc[x.project].iloc[0] * 100, axis=1)

print(df_inferred)
print(df_inferred['expkind'].describe())

#%% generate the boxplot
set_style()

plt.figure()
fig, ax = plt.subplots(1,1)

df_sorted = df_inferred[['expkind', 'percent']]
sorted_index = df_sorted.groupby('expkind') \
    .median() \
    .sort_values(by='percent', ascending=False) \
    .index

sns.boxplot(
    y='expkind',
    x='percent',
    data=df_sorted,
    order=sorted_index,
    ax=ax,
    showfliers=False)

ax.set_ylabel('')
ax.set_xlabel('Percent of inferred variable assignments (per project)')
import matplotlib.ticker as mtick
ax.xaxis.set_major_formatter(mtick.PercentFormatter())

save_figure(fig, 'rq-rhs-types.pdf', 7, 4)
fig

# %%
