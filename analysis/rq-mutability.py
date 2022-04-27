#!/usr/bin/env python
# coding: utf-8

from utils import *
from matplotlib.ticker import PercentFormatter

from scipy.stats import shapiro

set_style()

summarized = load_pre_summarized('kotlin', ['project', 'location', 'isval', 'isinferred'])
summarized = summarized[summarized['location'] != 'Return Type']
summarized = summarized[summarized['location'] != 'Lambda Args']
summarized = summarized[summarized['location'] != 'Loop Var']

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

rows = []

for location in summarized['location'].unique():
    for isinferred in summarized['isinferred'].unique():
        for isval in summarized['isval'].unique():
            stat, p = shapiro(summarized[(summarized['location'] == location) & (summarized['isinferred'] == isinferred) & (summarized['isval'] == isval)]['percent'])
            rows.append(pd.DataFrame({'Location': [location],
                                      'Inference?': [isinferred],
                                      'Var/Val?': [isval],
                                      'W': [stat],
                                      'p': [p],
                                      'Normal?': [ 'Yes' if p < 0.05 else 'No']}))

save_table(pd.concat(rows), 'tables/rq-mutability-shapiro.tex')
