#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
import pandas as pd

from common.df import get_deduped_df
from common.tables import get_styler, highlight_cols, highlight_rows, save_table


pd.set_option('display.max_colwidth', None)

df = get_deduped_df('method-calls-maybe-local', 'kotlin', header='infer')
df = df[['maybelocal']].count()


# %% generate the table
styler = highlight_rows(highlight_cols(get_styler(df)))
save_table(styler, 'rq-rhs-methodcalls.tex')

# %%
