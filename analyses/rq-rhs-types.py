#!/usr/bin/env python
#coding: utf-8
import numpy as np
import pandas as pd
from common.tables import *
from common.df import *
pd.set_option('display.max_colwidth', None)

df = get_df("determine-rhs-expression-types", "kotlin", header='infer')