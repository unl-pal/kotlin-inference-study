#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from common.tables import *
from common.df import *

df = get_df('counts', 'kotlin', header='infer')

df['filtered'] = df['filtered'].apply(lambda x: 'Post-Filtering' if x else 'Pre-Filtering')
df['type'] = df['type'].apply(lambda x: {'projects': 'Projects',
                                         'total_files_head': 'Source Files (HEAD)',
                                         'total_files_hist': 'Snapshots (HIST)'}[x])

df_pivot = df.pivot(index=['type'], columns=['filtered'])

df_pivot = df_pivot.reindex(['Projects',
                             'Source Files (HEAD)',
                             'Snapshots (HIST)'])

df_pivot = df_pivot.sort_index(axis='columns',
                               level='filtered',
                               ascending=False)

df_pivot = df_pivot.xs('count', axis='columns', drop_level=True)

# %% generate the table
styler = highlight_rows(highlight_cols(get_styler(df_pivot)))
save_table(styler, 'dataset-counts.tex', subdir='kotlin')

# %%
