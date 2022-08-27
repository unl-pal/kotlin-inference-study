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
from matplotlib import pyplot as plt
import os
import seaborn as sns

from .utils import _resolve_dir, _get_dir

__all__ = [
    'save_figure',
    'setup_plots'
]


def setup_plots(rcParams=None, constrained_layout=True, **subplotkw):
    sns.set_theme(context='paper', style='whitegrid', palette='colorblind')
    sns.set(font_scale=1.2)

    plt.rcParams['figure.figsize'] = [7.0, 4.0]
    plt.rcParams['figure.dpi'] = 600.0
    plt.rcParams['font.size'] = 24
    if rcParams:
        for (k, v) in rcParams.items():
            plt.rcParams[k] = v

    plt.figure()
    return plt.subplots(constrained_layout=constrained_layout, **subplotkw)


def save_figure(figure, filename, x=None, y=None, subdir=None):
    '''Save a FIGURE to FILENAME with size of X, Y inches.'''
    fig = figure.get_figure()
    if x is not None:
        fig.set(figwidth=x)
    if y is not None:
        fig.set(figheight=y)
    os.makedirs(_resolve_dir(f'figures/{_get_dir(subdir)}'), 0o755, True)
    fig.savefig(_resolve_dir(f'figures/{_get_dir(subdir)}{filename}'), dpi=600)
    plt.close(fig)
