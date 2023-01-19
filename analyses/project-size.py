#!/usr/bin/env python
# coding: utf-8

from common.tables import *
from common.graphs import setup_plots, save_figure
from common.df import *

import pandas as pd
import seaborn as sns

df_java = get_df('project-size', 'java', header='infer')
df_java_stars = get_df('stars', 'java', header='infer').rename(columns={'stars': 'count'})
df_java_stars['count_type'] = 'stars'
df_java_devs = get_df('developer-count', 'java', header='infer').rename(columns={'developers': 'count'})
df_java_devs['count_type'] = 'devs'
df_java = pd.concat([df_java, df_java_stars, df_java_devs])
df_java['language'] = 'Java'

df_kotlin = get_df('project-size', 'kotlin', header='infer')
df_kotlin_stars = get_df('stars', 'kotlin', header='infer').rename(columns={'stars': 'count'})
df_kotlin_stars['count_type'] = 'stars'
df_kotlin_devs = get_df('developer-count', 'kotlin', header='infer').rename(columns={'developers': 'count'})
df_kotlin_devs['count_type'] = 'devs'
df_kotlin = pd.concat([df_kotlin, df_kotlin_stars, df_kotlin_devs])
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
ax.set_xscale('log')
ax.set_ylabel('')
ax.set_xlabel('Number of Files')
save_figure(fig, 'project-files-summary.pdf')

fig, ax = setup_plots()
sns.boxplot(x='count',
            y='language',
            data=df_counts.loc[df_counts.count_type=='statements'],
            ax=ax,
            showfliers=False)
ax.set_xscale('log')
ax.set_ylabel('')
ax.set_xlabel('Number of Statements')
save_figure(fig, 'project-statements-summary.pdf')

fig, ax = setup_plots()
sns.boxplot(x='count',
            y='language',
            data=df_counts.loc[df_counts.count_type=='analyzed_commits'],
            ax=ax,
            showfliers=False)
ax.set_xscale('log')
ax.set_ylabel('')
ax.set_xlabel('')
save_figure(fig, 'project-commits-summary.pdf', y=1.4)

df_counts.count_type = df_counts.count_type.apply(lambda x: {'analyzed_commits': "Analyzed Commits",
                                                             'files': "Number of Files",
                                                             'statements': "Number of Statements",
                                                             'stars': "Number of Stars",
                                                             'devs': "Number of Committers"}[x])
df_summarized = df_counts.groupby(['language', 'count_type'])[['count']].describe()
df_summarized = drop_outer_column_index(df_summarized).drop(columns=['count'])
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
ax.set_xlabel('')
save_figure(fig, 'project-age-summary.pdf', y=1.4)

df_summarized_age = df_age.groupby(['language'])[['age']].describe()
summarized_age_styler = highlight_cols(highlight_rows(get_styler(drop_outer_column_index(df_summarized_age))))
save_table(summarized_age_styler, 'project-age-summary.tex')
