# coding: utf-8

import os
from typing import Optional


__all__ = [
    "_resolve_dir",
    "_get_dir",
]

def _resolve_dir(dir: str):
    curdir = os.getcwd()
    parts = curdir.split('/analyses')
    if len(parts) == 1:
        return dir
    return ''.join(['../' for x in range(len(parts))]) + dir


def _get_dir(subdir: Optional[str]):
    if subdir is None:
        return ''
    return subdir + '/'
