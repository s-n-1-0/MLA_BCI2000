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
                     subject='Subject', correction="auto", effsize="np2")
aov

# %%

grouped = read_data()
grouped.insert(0,"クラスタ",None)
for a in a_groups: grouped.loc[a,'クラスタ'] = "A"
for b in b_groups: grouped.loc[b,'クラスタ'] = "B"

# %%
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.conversion import py2rpy
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
with localconverter(robjects.default_converter + pandas2ri.converter):
    r_df = py2rpy(grouped)
    robjects.r.assign("df", r_df)
robjects.r("df")
robjects.r('source(file="C:/test/anovakun_489.txt")')
robjects.r('anovakun(df, "AsB", 2, 16)')
