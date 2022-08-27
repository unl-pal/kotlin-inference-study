# coding: utf-8

from matplotlib import pyplot as plt
import os.path as osp
import pandas as pd
import seaborn as sns

from .df import get_df
from .utils import _resolve_dir, _get_dir

__all__ = [
    'load_total_counts',
    'load_pre_summarized',
    'location_map',
    'inferred_name',
    'val_or_var',
    'plt',
    'sns'
]


def load_total_counts(language):
    path = _resolve_dir(f'data/parquet/{_get_dir(language)}total-counts.parquet')
    if osp.exists(path):
        return pd.read_parquet(path)
    df = get_df('basic-usage', language, header='infer')
    df_counts = df.groupby(['project', 'location'], as_index=False) \
        .sum()[['project', 'location', 'count']] \
        .rename(columns={'count': 'total'})[['project', 'location', 'total']]
    df_counts.to_parquet(path)
    return df_counts


def load_pre_summarized(language, group_cols):
    group_cols_string = '-'.join(group_cols)
    path = _resolve_dir(f'data/parquet/{_get_dir(language)}counts-summarized-{group_cols_string}.parquet')
    if osp.exists(path):
        return pd.read_parquet(path)
    df = get_df('basic-usage', language, header='infer')
    df_totals = load_total_counts(language)
    df_counted = df.groupby(group_cols, as_index=False).sum()[[*group_cols, 'count']]
    df_summarized = df_counted.merge(
        df_totals,
        on=['project', 'location'],
        how='left')
    df_summarized['percent'] = df_summarized.apply(
        lambda x: 0 if x['total'] == 0 else (x['count'] / x['total']) * 100,
        axis=1)
    if 'isinferred' in group_cols:
        df_summarized['isinferred'] = df_summarized['isinferred'].apply(inferred_name)
    if 'isval' in group_cols:
        df_summarized['isval'] = df_summarized['isval'].apply(val_or_var)
    if 'location' in group_cols:
        df_summarized['location'] = df_summarized['location'].apply(location_map)
    df_summarized.to_parquet(path)
    return df_summarized


def location_map(name):
    return {'return_val': 'Return Type',
            'body': 'Body',
            'module': 'Top Level',
            'lambda_arg': 'Lambda Args',
            'loop_variable': 'Loop Var'}[name]


def inferred_name(isinferred):
    return 'Inferred' if isinferred else 'Not Inferred'


def val_or_var(isval):
    return 'val' if isval else 'var'
