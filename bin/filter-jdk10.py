#!/usr/bin/env python3
# coding: utf-8

import sys

with open(sys.argv[1], 'r') as f:
    for id in [l.split('=')[-1].strip() for l in f.readlines()]:
        print(f'add(jdk10projects, "{id}");')
