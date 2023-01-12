#!/usr/bin/env python
# coding: utf-8

from common.tables import *
from common.graphs import setup_plots, save_figure
from common.df import *

import pandas as pd
import numpy as np
import seaborn as sns

from scipy.stats import pearsonr

for language in ['java', 'kotlin']:
    df_usage = get_deduped_df('basic-usage', language, header='infer')
    df = get_df('project-size', language, header='infer').pivot(index=['project'], columns=['count_type'], values=['count'])

    java_project_spots = df_usage.groupby('project')['count'].sum()
    java_used_spots = df_usage[df_usage.isinferred].groupby('project')['count'].sum()
    java_project_percent = java_used_spots.div(java_project_spots).mul(100)

    df['usage_percent'] = java_project_percent

    for factor in ['files', 'statements']:
        fig, ax = setup_plots()
        sns.regplot(x='usage_percent',
                    y=factor,
                    data=df,
                    fit_reg = True)
        r, p = pearsonr(df['usage_percent'],
                        df[factor])
        ax.set_title(f'Correlation between Percent Inferred and {factor}\n$r = {r}$ ($p = {p}$)')
        save_figure(fig, f'correlation_{factor}.pdf', language)
