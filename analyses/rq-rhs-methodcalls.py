#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
import pandas as pd

from common.df import get_deduped_df
from common.tables import get_styler, highlight_cols, highlight_rows, save_table


pd.set_option('display.max_colwidth', None)

df = get_deduped_df('method-calls-maybe-local', 'kotlin', header='infer')
df2 = df[['project', 'maybelocal']].groupby('maybelocal').count()
df2 = df2.rename(columns={'project': 'Number of Calls'})

# %% generate the table
styler = highlight_rows(highlight_cols(get_styler(df2)))
save_table(styler, 'rq-rhs-methodcalls.tex', subdir='kotlin')

# %%
