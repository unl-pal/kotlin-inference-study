#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
import pandas as pd
from common.graphs import setup_plots, save_figure
from common.tables import *
from common.df import *
from common.local import *
from matplotlib.ticker import PercentFormatter

pd.set_option('display.max_colwidth', None)

df = get_deduped_df('determine-rhs-expression-types', 'kotlin', header='infer')


def groupKinds(x):
    kind = x['expkind']
    if kind in ['ARRAYACCESS', 'CAST', 'LITERAL', 'METHODCALL', 'NEW', 'STATEMENT', 'VARACCESS']:
        return kind
    if kind == 'TEMPLATE':
        return 'LITERAL'
    if kind in ['ASSIGN', 'ASSIGN_ADD']:
        return 'STATEMENT'
    if kind == '??':
        return 'OTHER'
    if kind.startswith('OP_') or kind.startswith('BIT_') or kind.startswith('LOGICAL_'):
        return 'EXPRESSION'
    if kind in ['EQ', 'LTEQ', 'GTEQ', 'NEQ', 'GT', 'LT', 'PAREN', 'IN', 'NOT_IN', 'SHEQ', 'SHNEQ']:
        return 'EXPRESSION'
    return kind


df_inferred = df[df.isinferred == True].drop(columns=['isinferred', 'filepath', 'class'])
df_inferred['expkind'] = df_inferred.apply(groupKinds, axis=1)
df_inferred = df_inferred.groupby(['project', 'expkind'])['expkind'] \
    .count() \
    .reset_index(name='count')

sums = df_inferred.groupby(['project']) \
    .sum()
df_inferred['percent'] = df_inferred.apply(lambda x: x['count'] / sums.loc[x.project].iloc[0] * 100,
                                           axis=1)

print(df_inferred)

# %% generate the boxplot
fig, ax = setup_plots({'figure.figsize': [7.0, 6.0]})

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
ax.set_xlabel('Percent of inferred variable assignments\n(per project)')
ax.xaxis.set_major_formatter(PercentFormatter())

save_figure(fig, 'rq-rhs-types.pdf')
fig

# %%
