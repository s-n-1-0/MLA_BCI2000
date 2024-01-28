# %%
import pingouin as pg
import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
excel_path = "C:/Users/gomar/Downloads/1+2日目.xlsx"
subjects = 15
a_group = [3,5,8,10,11,12,16,17]
b_group = [1,2,4,7,9,13,15]
subjects = 15
pd.options.display.precision = 7
def read_data():
    return get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
read_data()
# %% 0.5水準とのt検定
data = read_data()
all_data = data.loc[a_group + b_group]
def ttest(i:int):
    a = all_data.values[:,i]
    b = np.array([0.5]*15)
    return pg.ttest(a, b, correction=False)
results = pd.concat([ttest(i) for i in range(16)])
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results.insert(3,"p-val(FDR/bh)",fdr[1])
fdr
results.to_csv("./results/0.5.csv")
results
# %%
data = read_data()
all_data = data.loc[a_group + b_group]
def ttest(i:int,j:int):
    a = all_data.values[:,i]
    b = all_data.values[:,j]
    df = pg.ttest(a, b, correction=False)
    df.index = [f"{(i+1)} vs. {(j+1)}"]
    return df
results = pd.concat([ttest(i,j) for i in range(16) for j in range(i+1,16)])
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results.insert(3,"p-val(FDR/bh)",fdr[1])
fdr
results.to_csv("./results/16times_diff.csv")
results
# %%
