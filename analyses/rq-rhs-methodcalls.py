#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from common.df import get_deduped_df
from common.tables import *

df_kotlin = get_deduped_df('method-calls-maybe-local', 'kotlin', header='infer')
df_kotlin = df_kotlin[['project', 'maybelocal']].groupby(['maybelocal']).count() \
                .rename(index={False: 'Not Local', True: 'Possibly File-Local'})
kotlin_total_calls = df_kotlin.project.sum()
df_kotlin['percent'] = df_kotlin.project.div(kotlin_total_calls).mul(100)
df_kotlin['formatted'] = df_kotlin.apply(lambda x: "{:,.0f} ({:,.2f}%)".format(x.project, x.percent), axis=1)
print(df_kotlin.formatted)

df_java = get_deduped_df('method-calls-maybe-local', 'java', header='infer')
df_java = df_java[['project', 'maybelocal']].groupby(['maybelocal']).count() \
                .rename(index={False: 'Not Local', True: 'Possibly File-Local'})
java_total_calls = df_java.project.sum()
df_java['percent'] = df_java.project.div(java_total_calls).mul(100)
df_java['formatted'] = df_java.apply(lambda x: "{:,.0f} ({:,.2f}%)".format(x.project, x.percent), axis=1)
print(df_java.formatted)

df_out = pd.DataFrame()
df_out['Kotlin'] = df_kotlin.formatted
df_out['Java'] = df_java.formatted

styler = highlight_rows(highlight_cols(get_styler(df_out)))
save_table(styler, 'rq-rhs-methodcalls.tex')
