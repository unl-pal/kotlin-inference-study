# coding: utf-8

# Copyright 2022, Robert Dyer,
#                 and University of Nebraska Board of Regents
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import Optional, Union, List
import pandas as pd

import seaborn as sns
import os.path as osp


def _get_dir(subdir: Optional[str]):
    if subdir is None:
        return ''
    return subdir + '/'

def get_df(filename: str, subdir: Optional[str]=None, header: Optional[Union[List[int], bool]]=None, **kwargs):
    '''Loads a CSV file into a DataFrame.

    Args:
        filename (str): the CSV file to load, without the '.csv' extension
        subdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that it lives in. Defaults to None.

    Returns:
        pd.DataFrame: the CSV file as a Pandas DataFrame
    '''
    try:
        df = pd.read_parquet(f'data/parquet/{_get_dir(subdir)}{filename}.parquet')
    except:
        df = pd.read_csv(f'data/csv/{_get_dir(subdir)}{filename}.csv', index_col=False, header=header, **kwargs)
        os.makedirs(f'data/parquet/{_get_dir(subdir)}', 0o755, True)
        df.to_parquet(f'data/parquet/{_get_dir(subdir)}{filename}.parquet', compression='gzip')
    return df

def get_deduped_df(filename: str, subdir: Optional[str]=None, ts=False, **kwargs):
    '''Loads a CSV file into a DataFrame and de-duplicates the data.

    This function assumes your table has columns named 'project' and 'file', and no column named 'hash'.

    Args:
        filename (str): the CSV file to load, without the '.csv' extension
        subdir (Optional[str], optional): the sub-directory, underneath 'data/csv/', that it lives in. Defaults to None.

    Returns:
        pd.DataFrame: the CSV file as a Pandas DataFrame
    '''
    try:
        df = pd.read_parquet(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet')
    except:
        if ts:
            df = _remove_dupes(get_df(filename, subdir, **kwargs), subdir, names=['var', 'hash', 'project', 'ts', 'file'])
        else:
            df = _remove_dupes(get_df(filename, subdir, **kwargs), subdir)
        os.makedirs(f'data/parquet/{_get_dir(subdir)}', 0o755, True)
        df.to_parquet(f'data/parquet/{_get_dir(subdir)}{filename}-deduped.parquet', compression='gzip')
    return df

def _remove_dupes(df: pd.DataFrame, subdir: Optional[str]=None, names=['var', 'hash', 'project', 'file']):
    df2 = get_df('dupes', subdir, names=names).drop(columns=['var'])

    df2 = df2[df2.duplicated(subset=['hash'])]
    df3 = pd.merge(df, df2, how='left', left_on=['project', 'file'], right_on=['project', 'file'])
    # df4 consists of rows in df3 where 'hash' is 'NaN' (meaning that they did not exist in df2.duplicated(subset=['hash']))
    df4 = df3[pd.isnull(df3['hash'])]
    return df4.drop(columns=['hash'])

_colsepname = ''
def save_table(df: pd.DataFrame, filename: str, subdir: Optional[str]=None, decimals=2, colsep: Union[bool, str]=False, **kwargs):
    '''Saves a DataFrame to a LaTeX table.

    Args:
        df (pd.DataFrame): The DataFrame to save as LaTeX.
        filename (str): The filename to save to, including '.tex' extension. Files are saved under 'tables/'.
        subdir (Optional[str], optional): the sub-directory, underneath 'tables/', to save in. Defaults to None.
        decimals (int, optional): How many decimal places for floats. Defaults to 2.
        colsep (Union[bool, str], optional): If False, use deafult column separators.  If a string, it is the column separator units. Defaults to False.
    '''
    global _colsepname
    if not colsep is False:
        _colsepname = _colsepname + 'A'

    pd.options.display.float_format = ('{:,.' + str(decimals) + 'f}').format

    with pd.option_context("max_colwidth", 1000):
        styled = df.style.applymap_index(lambda x: "textbf:--rwrap;", axis = 'columns')
        styled = styled.format_index(None, escape = 'latex', axis='columns')
        styled = styled.hide(names = True, axis = 'columns')
        styled = styled.applymap_index(lambda x: "textbf:--rwrap;", axis = 'index')
        styled = styled.format_index(None, escape = 'latex', axis='index')
        styled = styled.hide(names = True, axis = 'index')
        styled = styled.format(None, precision = decimals, thousands = ',', escape = 'latex')
        tab1 = styled.to_latex(hrules = hrules, multicol_align = multicol_align, **kwargs)

    os.makedirs(f'tables/{_get_dir(subdir)}', 0o755, True)
    with open(f'tables/{_get_dir(subdir)}{filename}', 'w', encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write('% this file was automatically generated\n')
        if not colsep is False:
            f.write('\\newcommand{\\oldtabcolsep' + _colsepname + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if not colsep is False:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + _colsepname + '}\n')

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

def load_total_counts(language):
    path = f"data/parquet/counts-{language}.parquet"
    if osp.exists(path):
        return pd.read_parquet(path)
    df = get_df("basic-usage", language)
    df_counts = df.groupby(['project', 'location'], as_index = False).sum()[['project', 'location', 'count']].rename(columns = {'count': 'total'})[['project', 'location', 'total']]
    df_counts.to_parquet(path)
    return df_counts

def load_pre_summarized(language, group_cols):
    group_cols_string = '-'.join(group_cols)
    path = f"data/parquet/counts-summarized-{language}-{group_cols_string}.parquet"
    if osp.exists(path):
        return pd.read_parquet(path)
    df = get_df("basic-usage", language)
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
