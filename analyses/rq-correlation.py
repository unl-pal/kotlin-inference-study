#!/usr/bin/env python
# coding: utf-8

from common.tables import *
from common.graphs import setup_plots, save_figure
from common.df import *

import pandas as pd
import numpy as np
import seaborn as sns

from scipy.stats import pearsonr

language_pretty = {'kotlin': 'Kotlin',
                   'java': 'Java'}

factor_pretty = {'files': '# files',
                 'statements': '# statements',
                 'stars': '# stars',
                 'developers': '# developers'}

out_frames = []

for language in ['kotlin', 'java']:
    df_size = pd.pivot_table(get_df('project-size', language, header='infer'),
                             index='project', columns='count_type', values='count')

    df_stars = get_df('stars', language, header='infer')
    df_num_devs = get_df('developer-count', language, header='infer')

    df_usage = get_deduped_df('basic-usage', language, header='infer')

    total_declarations = df_usage.groupby('project')['count'].sum()
    inferred_declarations = df_usage[df_usage.isinferred].groupby('project')['count'].sum()
    percent_annotated = inferred_declarations.div(total_declarations).mul(100).reset_index().rename(columns={'count': 'percent_annotated'})

    df = pd.merge(df_size, df_stars, on='project', how='inner')
    df = pd.merge(df, df_num_devs, on='project', how='inner')
    df = pd.merge(df, percent_annotated, on='project', how='inner')

    df = df.dropna()

    for factor in ['files', 'statements', 'stars', 'developers']:
        r, p = pearsonr(df['percent_annotated'], df[factor])
        out_frames.append(pd.DataFrame({'language': [language_pretty[language]],
                                        'factor': [factor_pretty[factor]],
                                        'r': [r],
                                        'p': [p]}))

df = pd.concat(out_frames).groupby(['language', 'factor']).sum()
styler = highlight_cols(highlight_rows(get_styler(df)))

save_table(styler, 'rq-correlations.tex')
