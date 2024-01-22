 # %%
import os
import numpy as np
import pandas as pd
import pingouin as pg
dir = "./predicts"
files = [f for f in os.listdir(dir) if ".npy" in f]
predicts = pd.DataFrame()
for f in files:
    predicts[f.replace(".npy","")] = np.load(f"{dir}/{f}")
predicts.to_csv(f"{dir}/predicts.csv")
predicts
# %%
vs_list1 = [("1st-1dcnn","1st-csplda"),
           ("1st-eegnet","1st-csplda"),
           ("1st-1dcnn","1st-eegnet")]
vs_list2 = [("2st-a-1dcnn","2st-b-1dcnn"),
           ("2st-b-1dcnn","2st-ft-1dcnn"),
           ("2st-a-1dcnn","2st-ft-1dcnn")]
def fdr_ttest(vs_list):
    results = []
    for vs1,vs2 in vs_list:
        result = pg.ttest(predicts[vs1].values, predicts[vs2].values, correction=False)
        result.index = [vs1 +" vs. " + vs2]
        results.append(result)
    results = pd.concat(results)
    results.insert(3,"p-val(FDR/bh)",None)
    fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
    results["p-val(FDR/bh)"] = fdr[1]
    return results
results1 = fdr_ttest(vs_list1)
results2 = fdr_ttest(vs_list2)
results1
# %%
results2
# %%
with pd.ExcelWriter(f'{dir}/ttest.xlsx') as writer:
    # 各データフレームを異なるシートとして保存
    results1.to_excel(writer, sheet_name='1st')
    results2.to_excel(writer, sheet_name='2st-1DCNN間')
# %% preview
key = "1st-eegnet"
np.mean(predicts[key]),np.std(predicts[key])