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

df_java = get_deduped_df('method-calls-maybe-local', 'java', header='infer')
df_java = df_java[['project', 'maybelocal']].groupby(['maybelocal']).count() \
                .rename(index={False: 'Not Local', True: 'Possibly File-Local'})
java_total_calls = df_java.project.sum()
df_java['percent'] = df_java.project.div(java_total_calls).mul(100)


df_out = pd.DataFrame()
df_out[('Java','Count')] = df_java.project
df_out[('Java','Percent')] = df_java.percent.apply(lambda x: "({:,.2f}%)".format(x))
df_out[('Kotlin','Count')] = df_kotlin.project
df_out[('Kotlin','Percent')] = df_kotlin.percent.apply(lambda x: "({:,.2f}%)".format(x))

styler = highlight_rows(highlight_cols(get_styler(df_out))).hide(axis='columns', level=1)
save_table(styler, 'rq-rhs-methodcalls.tex', column_format='lrrrr')
