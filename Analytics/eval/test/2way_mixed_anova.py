# %%
#
# 2要因混合分析
#
# %%
import pingouin as pg
import pandas as pd
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
# %%
excel_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
subjects = 15
a_groups = [3,5,8,10,11,12,16,17]
b_groups = [1,2,4,7,9,13,15]
def read_data():
    return get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
read_data()
# %%
_df = read_data()
groups = {}
for a in a_groups:groups[a] = "A"
for b in b_groups:groups[b] = "B"

df = pd.DataFrame(columns = ["Subject","Group","Time","Scores"])
for time in _df.columns:
    for s in groups.keys():
        df.loc[len(df)] = [s, groups[s], time,_df.loc[s,time]]
df
# %% 2要因混合計画
aov = pg.mixed_anova(data=df, dv='Scores', between='Group', within='Time',
                     subject='Subject', correction=False, effsize="n2")
aov
# %%
aov.to_csv("./results/2way_mixed_anova.csv")