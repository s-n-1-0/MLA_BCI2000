# %%
import pingouin as pg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
excel_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
a_group = [3,5,8,10,11,12,16,17]
b_group = [1,2,4,7,9,13,15]
subjects = 15
pd.options.display.precision = 7
def read_data():
    return get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
read_data()
# %%
data = read_data()
a_data = data.loc[a_group]
b_data = data.loc[b_group]
def ttest(i:int):
    a = a_data.values[:,i]
    b = b_data.values[:,i]
    return pg.ttest(a, b, correction=False)
results = pd.concat([ttest(i) for i in range(16)])
results.insert(3,"p-val(FDR/bh)",None)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/ttest_multicomp.csv")
results

# %% diffの差検定
a_diffdiffs = np.load("./diffdiffs_a.npy")
b_diffdiffs = np.load("./diffdiffs_b.npy")
plt.plot(range(8),np.mean(a_diffdiffs,axis=0),color="r")
plt.plot(range(8),np.mean(b_diffdiffs,axis=0))
def ttest(i:int):
    a = a_diffdiffs[:,i]
    b = b_diffdiffs[:,i]
    df = pg.ttest(a, b)
    df.index = [f"Day {i+1}"]
    return df
results = pd.concat([ttest(i) for i in range(8)])
results.insert(3,"p-val(FDR/bh)",None)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/diffdiff_ttest_multicomp.csv")
results
# %%
