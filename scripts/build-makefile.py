#!/usr/bin/env python
# coding: utf-8

from utilities import get_query_config, build_replacements

configuration = get_query_config()

for target in configuration['queries']:
    query_info = configuration['queries'][target]
    substitution_files = [x for (_, x) in build_replacements(configuration['substitutions'], query_info['substitutions'], only_files = True)]
    string = f"{query_info['query']}"
    for file_name in substitution_files:
        string += f" {file_name}"
    print(f"{target}: {string}\n\tpython3 scripts/download.py {target}")
