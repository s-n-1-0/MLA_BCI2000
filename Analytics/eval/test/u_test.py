# %%
import pingouin as pg
import pandas as pd
import sys
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
results
# %%
results.to_csv("./results/u_test.csv")