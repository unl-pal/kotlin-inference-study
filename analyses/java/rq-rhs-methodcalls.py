#!/usr/bin/env python
# coding: utf-8

# %% build the dataframe
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd

from common.df import get_deduped_df
from common.tables import *


pd.set_option('display.max_colwidth', None)

df = get_deduped_df('method-calls-maybe-local', 'java', header='infer')
df2 = df[['project', 'maybelocal']].groupby('maybelocal').count()
df2 = df2.rename(columns={'project': 'Number of Calls'})
df2 = df2.rename(index={False: 'Not Local', True: 'Possibly File-Local'})

# %% generate the table
styler = highlight_rows(highlight_cols(get_styler(df2)))
save_table(styler, 'rq-rhs-methodcalls.tex', subdir='java')

# %%
