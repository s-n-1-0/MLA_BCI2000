# %%
import pingouin as pg
import pandas as pd
import sys
import numpy as np
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
st12_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
st3_path = "C:/Users/2221012/Downloads/3日目.xlsx"
groups = [3,10,16]
st12_subjects = 15
st3_subjects = 3
pd.options.display.precision = 7
print(get_data_from_excel(st12_path,subjects=st12_subjects,iloc=17,index_col=0))
# %%
st12_data = get_data_from_excel(st12_path,subjects=st12_subjects,iloc=17,index_col=0)
st3_data = get_data_from_excel(st3_path,subjects=st3_subjects,iloc=17,index_col=0)
results = None
for m in groups:
    st12 = st12_data.loc[m].values
    st3 = st3_data.loc[m].values
    _results = pg.mwu(st12,st3)
    _results.index = [m]
    if results is None:
        results = _results
    else:
        results = pd.concat([results,_results])
results = results.drop(["RBC","CLES"],axis=1)
results.to_csv("./results/u_test.csv")
results

# %% DiffDiffのu検定
results = None
a_diffdiffs = np.load("./diffdiffs_a.npy")
b_diffdiffs = np.load("./diffdiffs_b.npy")
for i in range(8):
    _results = pg.mwu(a_diffdiffs[:,i],b_diffdiffs[:,i])
    _results.index = [" ".join([
        "1周目" if i < 4 else "2周目",
        f"{(i+1)%4 if (i+1) %4 != 0 else 4}日目"
    ])]
    if results is None:
        results = _results
    else:
        results = pd.concat([results,_results])
results = results.drop(["RBC","CLES"],axis=1)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/u_test.csv")
results
# %%
results = None
a_diffdiffs = np.load("./diffdiffs_a.npy")
b_diffdiffs = np.load("./diffdiffs_b.npy")
data = np.concatenate([a_diffdiffs,b_diffdiffs],axis=0)
def wilcoxon(diffdiffs:np.ndarray,i:int):
    day1 = diffdiffs[:,0]
    result = pg.wilcoxon(day1,diffdiffs[:,i] ,alternative="less")
    result.index = [" ".join(["1周目1日目 vs.",
        "1周目" if i < 4 else "2周目",
        f"{(i+1)%4 if (i+1) %4 != 0 else 4}日目"
    ])]
    return result
results = pd.concat([wilcoxon(data,i) for i in range(1,8)])
results = results.drop(["RBC","CLES"],axis=1)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/u_test_all.csv", encoding="shift-jis")

results = pd.concat([wilcoxon(a_diffdiffs,i) for i in range(1,8)])
results = results.drop(["RBC","CLES"],axis=1)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/u_test_cl1.csv",encoding="shift-jis")

results = pd.concat([wilcoxon(b_diffdiffs,i) for i in range(1,8)])
results = results.drop(["RBC","CLES"],axis=1)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/u_test_cl2.csv", encoding="shift-jis")
print(results)
# %%
def wilcoxon(diffdiffs:np.ndarray,i:int):
    z_statistic = (np.mean(diffdiffs[:,i]) - 0) / (np.std(diffdiffs[:,i]) / np.sqrt(len(diffdiffs[:,i])))
    result = pg.wilcoxon(diffdiffs[:,i])
    result.insert(0,"Z-val",z_statistic)
    result.index = [" ".join([
        "1周目" if i < 4 else "2周目",
        f"{(i+1)%4 if (i+1) %4 != 0 else 4}日目"
    ])]
    return result
results = pd.concat([wilcoxon(data,i) for i in range(8)])
results = results.drop(["RBC","CLES"],axis=1)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/u_test_all.csv", encoding="shift-jis")

results = pd.concat([wilcoxon(a_diffdiffs,i) for i in range(8)])
results = results.drop(["RBC","CLES"],axis=1)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/u_test_cl1.csv",encoding="shift-jis")

results = pd.concat([wilcoxon(b_diffdiffs,i) for i in range(8)])
results = results.drop(["RBC","CLES"],axis=1)
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
results["p-val(FDR/bh)"] = fdr[1]
results.to_csv("./results/u_test_cl2.csv", encoding="shift-jis")