#!/usr/bin/env python
# coding: utf-8

#%% build the dataframe
import pandas as pd
from common.tables import *
from common.df import *

df = get_df('counts', 'kotlin', header='infer')

df['filtered'] = df['filtered'].apply(lambda x: 'Post-Filtering' if x else 'Pre-Filtering')
df['type'] = df['type'].apply(lambda x: {'projects': 'Projects',
                                         'total_files_head': 'Total Files (HEAD)',
                                         'analyzed_files_head': 'Analyzed Files (HEAD)',
                                         'total_files_hist': 'Total Files (HIST)',
                                         'analyzed_files_hist': 'Analyzed Files (HIST)'}[x])

df_pivot = df.pivot(index = ['type'], columns = ['filtered'])

df_pivot = df_pivot.reindex(['Projects',
                             'Total Files (HEAD)',
                             'Analyzed Files (HEAD)',
                             'Total Files (HIST)',
                             'Analyzed Files (HIST)'])

df_pivot = df_pivot.sort_index(axis='columns', level='filtered', ascending=False)

df_pivot = df_pivot.xs('count', axis='columns', drop_level=True)

#%% generate the table
styler = highlight_rows(highlight_cols(get_styler(df_pivot)))
save_table(styler, 'dataset-counts.tex')

# %%
