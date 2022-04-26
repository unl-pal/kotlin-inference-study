#!/usr/bin/env python
# coding: utf-8

from utils import *
from matplotlib.ticker import PercentFormatter

set_style()

summarized = load_pre_summarized('kotlin', ['project', 'location', 'isval', 'isinferred'])
summarized = summarized[summarized['location'] != 'Return Type']

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
save_figure(figure.figure, "figures/rq-mutability-summary.pdf", 7, 4)

save_table(summarized[['location', 'isinferred', 'isval', 'percent']].groupby(['location', 'isinferred', 'isval']).describe(), "tables/rq-mutability-summary.tex")
