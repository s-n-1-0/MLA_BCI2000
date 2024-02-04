# %%
import pingouin as pg
import pandas as pd
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
    return pg.ttest(a, b)
results = pd.concat([ttest(i) for i in range(16)])
results.insert(3,"p-val(FDR/bh)",None)
results
# %%
fdr = pg.multicomp(results["p-val"].values, method='fdr_bh') 
fdr
# %%
results["p-val(FDR/bh)"] = fdr[1]
results

# %%
results.to_csv("./results/ttest_multicomp.csv")