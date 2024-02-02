# %%
import pingouin as pg
import pandas as pd
import numpy as np
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
excel_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
subjects = 15
a_group = [3,5,8,10,11,12,16,17]
b_group = [1,2,4,7,9,13,15]
subjects = 15
pd.options.display.precision = 7
def read_data():
    return get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
_df = read_data()
data = pd.DataFrame(columns = ["Subject","Time","Scores"])
for i,column in enumerate(_df.columns):
    for s in a_group + b_group:
        data.loc[len(data)] = [s,i+1,_df.loc[s,column]]
data
read_data()
# %% 0.5水準とのt検定
data = read_data()
all_data = data.loc[a_group + b_group]
def ttest(i:int):
    a = all_data.values[:,i]
    return pg.ttest(a, 0.5, correction=False)
results = pd.concat([ttest(i) for i in range(16)])
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results.insert(3,"p-val(FDR/bh)",fdr[1])
fdr
results.to_csv("./results/0.5.csv")
results
# %%
results = pg.pairwise_tests(dv='Scores', within='Time', subject='Subject', data=data)

fdr = pg.multicomp(results["p-unc"].values, method='fdr_bh') 
results.insert(8,"p-val(FDR/bh)",fdr[1])

results.to_csv("./results/16times_diff.csv")
results

# %%
data
# %%
