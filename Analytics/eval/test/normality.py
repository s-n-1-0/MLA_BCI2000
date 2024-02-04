# %%
# 正規性の検定
# Shapiro-Wilk
#
import numpy as np
import pingouin as pg
import pandas as pd
import sys
import math
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
excel_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
subjects = 15
pd.options.display.precision = 7
def read_data():
    return get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
# %%
data = read_data()
def normality(i:int):
    result = pg.normality(data.values[:,i])
    result.index = [" ".join([
        "1周目" if i < 8 else "2周目",
        f"{math.ceil((i+1 - (0 if i < 8 else 8))/2)}日目",
        "pre" if i % 2 == 0 else "post"
    ])]
    return result
results = pd.concat([normality(i) for i in range(16)])
results["p-val(FDR/bh)"] = None
results = results.drop("normal",axis=1)
results = results.rename(columns={"pval":"p-val"})
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/normality.csv")
results

# %%
a_diffdiffs = np.load("./diffdiffs_a.npy")
b_diffdiffs = np.load("./diffdiffs_b.npy")
data = np.concatenate([a_diffdiffs,b_diffdiffs],axis=0)
print(data.shape)
def normality(i:int):
    result = pg.normality(data[:,i])
    result.index = [" ".join([
        "1周目" if i < 4 else "2周目",
        f"{(i+1)%4 if (i+1) %4 != 0 else 4}日目"
    ])]
    return result
results = pd.concat([normality(i) for i in range(8)])
results["p-val(FDR/bh)"] = None
results = results.drop("normal",axis=1)
results = results.rename(columns={"pval":"p-val"})
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/diffdiffs_normality.csv")
results
# %%
