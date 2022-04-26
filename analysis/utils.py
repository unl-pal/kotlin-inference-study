#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os.path as osp

# Set default plot style
def set_style():
    sns.set_style('whitegrid')
    sns.set_palette('colorblind')

def save_figure(figure, filename, x=None, y=None):
    '''Save a FIGURE to FILENAME with size of X, Y inches.'''
    fig = figure.get_figure()
    plt.tight_layout()
    if x is not None:
        fig.set(figwidth = x)
    if y is not None:
        fig.set(figheight = y)
    fig.savefig(filename, dpi=600)
    plt.close(fig)

colsepname = ''
def save_table(df, filename, decimals=2, colsep=False, **kwargs):
    global colsepname
    if not colsep is False:
        colsepname = colsepname + 'A'

    pd.options.display.float_format = ('{:,.' + str(decimals) + 'f}').format

    with pd.option_context("max_colwidth", 1000):
        tab1 = df.style.format_index("\\textbf{{{0}}}", axis = 1).to_latex(**kwargs)
    # print(tab1)
    with open(filename,'w',encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write(f'% this file was automatically generated by Pandas on {datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ%z")}\n')
        if not colsep is False:
            f.write('\\newcommand{\\oldtabcolsep' + colsepname + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if not colsep is False:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + colsepname +'}\n')


def load_data_csv(language, file, **kwargs):
    return pd.read_csv(f"data-csv/{language}/{file}", on_bad_lines='skip', **kwargs)

def load_usage_data(language):
    path = f"data-csv/cached/usage-{language}.parquet"
    if osp.exists(path):
        return pd.read_parquet(path)
    df = load_data_csv(language, "basic-usage.csv")
    df.to_parquet(path)
    return df

def load_total_counts(language):
    path = f"data-csv/cached/counts-{language}.parquet"
    if osp.exists(path):
        return pd.read_parquet(path)
    df = load_usage_data(language)
    df_counts = df.groupby(['project', 'location'], as_index = False).sum()[['project', 'location', 'count']].rename(columns = {'count': 'total'})[['project', 'location', 'total']]
    df_counts.to_parquet(path)
    return df_counts

def load_pre_summarized(language, group_cols):
    group_cols_string = '-'.join(group_cols)
    path = f"data-csv/cached/counts-summarized-{language}-{group_cols_string}.parquet"
    if osp.exists(path):
        return pd.read_parquet(path)
    df = load_usage_data(language)
    df_totals = load_total_counts(language)
    df_counted = df.groupby(group_cols, as_index = False).sum()[[*group_cols, 'count']]
    df_summarized = df_counted.merge(df_totals, on=['project', 'location'], how = 'left')
    df_summarized['percent'] = df_summarized.apply(lambda x: 0 if x['total'] == 0 else (x['count'] / x['total']) * 100, axis = 1)
    if 'isinferred' in group_cols:
        df_summarized['isinferred'] = df_summarized['isinferred'].apply(inferred_name)
    if 'isval' in group_cols:
        df_summarized['isval'] = df_summarized['isval'].apply(val_or_var)
    if 'location' in group_cols:
        df_summarized['location'] = df_summarized['location'].apply(location_map)
    df_summarized.to_parquet(path)
    return df_summarized

def location_map(name):
    return {'return_val': "Return Type",
            'body': "Body",
            'module': "Top Level",
            'lambda_arg': "Lambda Args",
            'loop_variable': "Loop Var"}[name]

def inferred_name(isinferred):
    return 'Inferred' if isinferred else 'Not Inferred'

def val_or_var(isval):
    return 'val' if isval else 'var'
