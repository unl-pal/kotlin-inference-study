#!/usr/bin/env python
#coding: utf-8
#%%
import pandas as pd
from common.tables import *
from common.df import *
from common.local import *
pd.set_option('display.max_colwidth', None)

df = get_df('determine-rhs-expression-types', 'kotlin', header='infer')

set_style()

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

df_count = df[df.isinferred == True].drop(columns=['isinferred', 'filepath', 'class', 'count'])
df_count['expkind'] = df_count.apply(groupKinds, axis=1)
df_count = df_count.groupby(['project', 'expkind'])['expkind'].count().reset_index(name='count')
sums = df_count.groupby(['project']).sum()
df_count['percent'] = df_count.apply(lambda x: x['count'] / sums.loc[x.project].iloc[0] * 100, axis=1)
print(df_count)
print(df_count['expkind'].describe())
#df[(df.expkind == '??') & (df.isinferred == False)]
#df[(df.expkind == '??') & (df.isinferred == True)]

#%%
plt.figure()
fig, ax = plt.subplots(1,1)
plt.xticks(rotation=45, horizontalalignment='right')

df_sorted = df_count[['expkind', 'percent']]
sorted_index = df_sorted.groupby('expkind').median().sort_values(by='percent', ascending=False).index
sns.boxplot(x='expkind', y='percent', data=df_sorted, order=sorted_index, ax=ax, showfliers=False)

ax.set_ylabel('Percent per Project')
ax.set_xlabel('')
save_figure(fig, 'rq-rhs-types.pdf', 7, 4)
fig

# %%
