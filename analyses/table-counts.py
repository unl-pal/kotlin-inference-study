#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from common.tables import *
from common.df import *

df_unfiltered = get_df("count-unfiltered", "kotlin", header='infer')
df_filtered = df_get("count-filtered", "kotlin", header='infer')

df = pd.concat([df_unfiltered, df_filtered])
df['filtered'] = df['filtered'].apply(lambda x: "Post-Filtering" if x else "Pre-Filtering")
df['type'] = df['type'].apply(lambda x: {'projects': "Projects",
                                         'total_files_head': "Total Files (HEAD)",
                                         'analyzed_files_head': "Analyzed Files (HEAD)",
                                         'total_files_hist': "Total Files (HIST)",
                                         'analyzed_files_hist': "Analyzed Files (HIST)"}[x])
df_pivot = df.pivot(index = ['type'], columns = ['filtered'])

styler = highlight_rows(highlight_cols(get_styler(df_pivot)))
save_table(styler, "dataset-counts.tex")
