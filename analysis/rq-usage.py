#!/usr/bin/env python
# coding: utf-8

from utils import *
from matplotlib.ticker import PercentFormatter

set_style()

summarized = load_pre_summarized('kotlin', ['project', 'location', 'isinferred'])

plt.figure()
fig, ax = plt.subplots(1,1)
sns.boxplot(x='location', y='percent', hue='isinferred', data=summarized, ax = ax, showfliers = False)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_ylabel("Percent per Project")
ax.set_xlabel("")
plt.gca().legend().set_title("")
save_figure(fig, "figures/rq-usage-summary.pdf", 7, 4)

save_table(summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe(), "tables/rq-usage-summary.tex")
