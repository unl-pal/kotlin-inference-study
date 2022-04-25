#!/usr/bin/env python
# coding: utf-8

from utils import *
from matplotlib.ticker import PercentFormatter

set_style()

df = load_data_csv("kotlin", "basic-usage.csv")

total_counts = df.groupby(['project', 'location'], as_index = False).sum()[['project', 'location', 'count']].rename(columns = {'count': 'total'})
counted = df.groupby(['project', 'location', 'isinferred'], as_index = False).sum()[['project', 'location', 'isinferred', 'count']]
summarized = counted.merge(total_counts, on=['project', 'location'], how='left')
summarized['percent'] = summarized.apply(lambda x: (x['count'] / x.total) * 100, axis = 1)
summarized['isinferred'] = summarized.apply(lambda x: 'Inferred' if x.isinferred else 'Not Inferred', axis = 1)
summarized['location'] = summarized.apply(lambda x: {'return_val': "Return Value", 'body': "Body", 'module': "Module", 'lambda_arg': "Lambda Argument"}[x.location], axis = 1)
plt.figure()
fig, ax = plt.subplots(1,1)
sns.boxplot(x='location', y='percent', hue='isinferred', data=summarized, ax = ax, showfliers = False)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_ylabel("Percent per Project")
ax.set_xlabel("")
plt.gca().legend().set_title()
save_figure(fig, "figures/rq-usage-summary.pdf", 7, 4)
