#%%
import numpy as np
import pandas as pd
from common.tables import *
from common.df import *
pd.set_option('display.max_colwidth', None)

df = pd.read_csv(r"right-hand-side-expression.csv", names=['id', 'file_path', 'isInferred', 'expressionKind', 'methodName', 'count'])
df = df[df.isInferred == "true"]

expressionCategories = pd.DataFrame()
expressionCategories['Category'] = ['Literal', 'Constructor', 'NEW', 'Other']
expressionCategories

counts = []

numLiterals = len(df[df.expressionKind == 'LITERAL'])
counts.append(numLiterals)

# numConstructors = len(df[(df.expressionKind == 'NEW') | (df['methodName'].astype(str).str[0].str.isupper())])
numConstructors = len(df[df.methodName.astype(str).str[0].str.isupper()])
counts.append(numConstructors)

numNEW = len(df[df.expressionKind == 'NEW'])
counts.append(numNEW)

# numOther = len(df[(df.expressionKind != 'LITERAL') & (df.expressionKind != 'NEW') & (df.expressionKind != 'METHODCALL')])
numOther = len(df) - numLiterals- numConstructors - numNEW
counts.append(numOther)

expressionCategories['Count'] = counts
expressionCategories

# save_table(expressionCategories, "expression-categories.tex")
