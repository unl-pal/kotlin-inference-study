#!/usr/bin/env python
# coding: utf-8

from common.tables import *
from common.graphs import setup_plots, save_figure
from common.df import *

import pandas as pd
import numpy as np
import seaborn as sns

df_java = get_df('project-size', 'java', header='infer')
df_java['language'] = 'Java'

df_kotlin = get_df('project-size', 'kotlin', header='infer')
df_kotlin['language'] = 'Kotlin'

df = pd.concat([df_java, df_kotlin]).reset_index()
df_counts = df.loc[df.count_type != 'project_age'].copy(deep=True)
df_age = df.loc[df.count_type == 'project_age'].copy(deep=True)

fig, ax = setup_plots()
sns.boxplot(x='count',
            y='language',
            data=df_counts.loc[df_counts.count_type=='files'],
            ax=ax,
            showfliers=False)
ax.xscale('log')
ax.set_ylabel('')
ax.set_xlabel('Number of Files')
save_figure(fig, 'project-files-summary.pdf')

fig, ax = setup_plots()
sns.boxplot(x='count',
            y='language',
            data=df_counts.loc[df_counts.count_type=='statements'],
            ax=ax,
            showfliers=False)
ax.xscale('log')
ax.set_ylabel('')
ax.set_xlabel('Number of Statements')
save_figure(fig, 'project-statements-summary.pdf')

fig, ax = setup_plots()
sns.boxplot(x='count',
            y='language',
            data=df_counts.loc[df_counts.count_type=='analyzed_commits'],
            ax=ax,
            showfliers=False)
ax.xscale('log')
ax.set_ylabel('')
ax.set_xlabel('Number of Analyzed Commits')
save_figure(fig, 'project-commits-summary.pdf')

df_counts.count_type = df_counts.count_type.apply(lambda x: {'analyzed_commits': "Analyzed Commits",
                                                             'files': "# of Files",
                                                             'statements': "# of Statements"}[x])
df_summarized = df_counts.groupby(['language', 'count_type'])[['count']].describe()
summarized_styler = highlight_cols(highlight_rows(get_styler(df_summarized)))
save_table(summarized_styler, 'project-size-summary.tex')

df_age['age'] = pd.to_timedelta(df['count'], unit='us').apply(lambda x: x.days/365.254)

fig, ax = setup_plots()
sns.boxplot(x='age',
            y='language',
            data=df_age,
            ax=ax,
            showfliers=False)
ax.set_ylabel('')
ax.set_xlabel('Project Age in Years')
save_figure(fig, 'project-age-summary.pdf')

df_summarized_age = df_age.groupby(['language'])[['age']].describe()
summarized_age_styler = highlight_cols(highlight_rows(get_styler(df_summarized_age)))
save_table(summarized_age_styler, 'project-age-summary.tex')
