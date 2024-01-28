# %%
#
# 1要因 rm分散分析
#
import pingouin as pg
import pandas as pd
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
excel_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
subjects = 15
a_group = [3,5,8,10,11,12,16,17]
b_group = [1,2,4,7,9,13,15]
def read_data():
    return get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
read_data()
# %%
results = []
for gorup_mode in [True,False,None]: #A:True,B:False,全員:None
    _df = read_data()
    df = pd.DataFrame(columns = ["Subject","Time","Scores"])
    for time in _df.columns:
        group = a_group + b_group
        if gorup_mode is not None: group = (a_group if gorup_mode else b_group)
        for s in group:
            df.loc[len(df)] = [s, time,_df.loc[s,time]]
    df
    # 1要因 rm分散分析
    if gorup_mode is None : print("全員")
    else: print("A" if gorup_mode else "B")
    aov = pg.rm_anova(data=df, dv='Scores', within='Time', subject='Subject', detailed=True,effsize="n2")
    results.append(aov)
# %%
for key, aov in zip(["Cl1","Cl2","All"],results):
    aov.to_csv(f"./results/rm_anova_{key}.csv")