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
is_a = True
a_groups = [3,5,8,10,11,12,16,17]
b_groups = [1,2,4,7,9,13,15]
def read_data():
    return get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
read_data()
# %%
_df = read_data()
df = pd.DataFrame(columns = ["Subject","Time","Scores"])
for time in _df.columns:
    for s in (a_groups if is_a else b_groups):
        df.loc[len(df)] = [s, time,_df.loc[s,time]]
df
# %% 1要因 rm分散分析
print("A" if is_a else "B")
aov = pg.rm_anova(data=df, dv='Scores', within='Time', subject='Subject', detailed=True,effsize="n2")
aov

# %%
