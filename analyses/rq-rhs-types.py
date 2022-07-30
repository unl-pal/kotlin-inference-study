#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from common.tables import *
from common.df import *
pd.set_option('display.max_colwidth', None)

# df = get_df("right-hand-side-expression", "kotlin", names=['id', 'file_path', 'isInferred', 'expressionKind', 'methodName', 'count'])
df = get_df("determine-rhs-expression-types", "kotlin", names=['project_id', 'file_url', 'class', 'isinferred', 'isactualvar', 'expkind', 'vartype', 'mapval', 'count'])
df = df[df.isInferred == "true"]

expressionCategories = pd.DataFrame()
expressionCategories['Category'] = ['Literal', 'Constructor', 'NEW', 'Other']

counts = []

numLiterals = len(df[df.expressionKind == 'LITERAL'])
counts.append(numLiterals)

numConstructors = len(df[df.methodName.astype(str).str[0].str.isupper()])
counts.append(numConstructors)

numNEW = len(df[df.expressionKind == 'NEW'])
counts.append(numNEW)

numOther = len(df) - numLiterals- numConstructors - numNEW
counts.append(numOther)

expressionCategories['Count'] = counts
print(expressionCategories)
styler = highlight_rows(highlight_cols(get_styler(expressionCategories)))
save_table(styler, "expression-categories.tex")
