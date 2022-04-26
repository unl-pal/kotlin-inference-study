#!/usr/bin/env python
# coding: utf-8

from utils import *
from matplotlib.ticker import PercentFormatter

set_style()

df = load_usage_data("kotlin")
total_counts = load_total_counts("kotlin")

counted = df.groupby(['project', 'location', 'isval', 'isinferred'], as_index = False).sum()[['project', 'location', 'isval', 'isinferred', 'count']]

summarized = counted.merge(total_counts, on=['project', 'location'], how = 'left')
summarized['percent'] = summarized.apply(lambda x: 0 if x['total'] == 0 else (x['count'] / x['total']) * 100, axis = 1)
summarized['isinferred'] = summarized.apply(lambda x: 'Inferred' if x.isinferred else 'Not Inferred', axis = 1)
summarized['isval'] = summarized.apply(lambda x: 'val' if x.isval else 'var', axis = 1)
summarized['location'] = summarized.apply(lambda x: {'return_val': "Return Value", 'body': "Body", 'module': "Top-Level Variables", 'lambda_arg': "Arguments List in Lambda", 'loop_variable': "Loop Variable"}[x.location], axis = 1)

summarized = summarized[summarized['location'] != 'Return Value']

plt.figure()
# fig, ax = plt.subplots(1, 1)
figure = sns.catplot(x = 'location', y = 'percent', hue = 'isinferred', col = 'isval', data = summarized,
                     sharey = True,
                     showfliers = False, kind = 'box')
figure.set_ylabels("Percent per Project")
figure.set_xlabels("")
figure.legend.set_title("")
for ax in figure.axes.flat:
    ax.yaxis.set_major_formatter(PercentFormatter(100))
save_figure(figure, "figures/rq-mutability-summary.pdf", 7, 4)

save_table(summarized[['location', 'isinferred', 'isval', 'percent']].groupby(['location', 'isinferred', 'isval']).describe(), "tables/rq-mutability-summary.tex")
