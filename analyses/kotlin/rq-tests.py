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
import matplotlib.ticker as mtick

df_tests = get_df('tests', 'kotlin', header='infer')

df_orig = get_df('basic-usage', 'kotlin', header='infer')
df = df_tests.merge(df_orig, how='left', on=['project', 'file'])

df_totals = df.groupby(['project', 'location'])[['count']].sum().rename(columns={'count':'total'}).reset_index()

df_counted = df.groupby(['project', 'location', 'isinferred'], as_index=False).sum()[['project', 'location', 'isinferred', 'count']]

df_temp = pd.merge(pd.merge(pd.Series(df_counted.project.unique(), name='project'),
                            pd.Series(df_counted.location.unique(), name='location'), how='cross'),
                   pd.Series(df_counted.isinferred.unique(),name='isinferred'), how='cross')

df_counted = df_counted.merge(df_temp,
                              on=['project', 'location', 'isinferred'],
                              how='right') \
                       .fillna(0)

print(df_counted.head())
                              

df_summarized = df_counted.merge(
    df_totals,
    on=['project', 'location'],
    how='outer')

print(df_summarized.head())
df_summarized = df_summarized[df_summarized.total > 0]

df_summarized['percent'] = df_summarized.apply(
    lambda x: 0 if x['total'] == 0 else (x['count'] / x['total']) * 100,
    axis=1)
df_summarized['isinferred'] = df_summarized['isinferred'].apply(inferred_name)
df_summarized['location'] = df_summarized['location'].apply(location_map)

summarized = df_summarized

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
save_figure(fig, 'rq-usage-tests.pdf', subdir='kotlin')
fig

# %% generate the table
data = summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe()
styler = highlight_cols(highlight_rows(get_styler(drop_count_if_same(drop_outer_column_index(data)))))

save_table(styler, 'rq-usage-tests.tex', subdir='kotlin')
