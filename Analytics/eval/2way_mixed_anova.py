# %%
#
# TODO: 2要因混合分析をやる
#
# %%
import pingouin as pg
# %%
df = pg.read_dataset('mixed_anova')
df
# %%
aov = pg.mixed_anova(data=df, dv='Scores', between='Group', within='Time',
                     subject='Subject', correction=False, effsize="np2")
aov

# %%

df.reindex(columns=['Subject', 'Group', 'Time','Scores'])
grouped = df.groupby(['Subject','Group'])['Scores'].apply(list).reset_index()


max_len = grouped['Scores'].str.len().max()
for i in range(max_len):
    grouped[f'Scores{i+1}'] = grouped['Scores'].apply(lambda x: x[i] if i < len(x) else None)

grouped.drop(columns=['Subject','Scores'], inplace=True)# 最初のリスト列を削除
grouped

# %%
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.conversion import py2rpy
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
with localconverter(robjects.default_converter + pandas2ri.converter):
    r_df = py2rpy(grouped)
    robjects.r.assign("df", r_df)
robjects.r("df")
robjects.r('options(encoding = "utf-8")')
robjects.r('source(file="C:/test/anovakun_489.txt")')
robjects.r('anovakun(df, "AsB", 2, 3)')