# %%
import pingouin as pg
import pandas as pd
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
st12_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
st3_path = "C:/Users/2221012/Downloads/3日目.xlsx"
groups = [10]
st12_subjects = 15
st3_subjects = 3
pd.options.display.precision = 7
print(get_data_from_excel(st12_path,subjects=st12_subjects,iloc=17,index_col=0))
# %%
st12_data = get_data_from_excel(st12_path,subjects=st12_subjects,iloc=17,index_col=0)
st3_data = get_data_from_excel(st3_path,subjects=st3_subjects,iloc=17,index_col=0)
st12_data = st12_data.loc[groups].values[0]
st3_data = st3_data.loc[groups].values[0]
pg.mwu(st12_data,st3_data)