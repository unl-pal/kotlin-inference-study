#!/usr/bin/env python
# coding: utf-8

from common.local import *
from common.tables import *
from matplotlib.ticker import PercentFormatter

from scipy.stats import shapiro

set_style()

summarized = load_pre_summarized('kotlin', ['project', 'location', 'isinferred'])

plt.figure()
fig, ax = plt.subplots(1,1)
sns.boxplot(x='location', y='percent', hue='isinferred', data=summarized, ax = ax, showfliers = False)
ax.yaxis.set_major_formatter(PercentFormatter(100))
ax.set_ylabel("Percent per Project")
ax.set_xlabel("")
plt.gca().legend().set_title("")
save_figure(fig, "rq-usage-summary.pdf", 7, 4)


styler = highlight_cols(highlight_rows(get_styler(summarized[['location', 'isinferred', 'percent']].groupby(['location', 'isinferred']).describe())))

save_table(styler, "rq-usage-summary.tex")
