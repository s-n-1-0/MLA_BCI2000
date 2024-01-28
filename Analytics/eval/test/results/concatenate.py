# %%
import os
import pandas as pd
dir = "./"
files = [f for f in os.listdir(dir) if ".csv" in f]
df_list = []
for f in files:
    df_list.append((f,pd.read_csv(f)))  

df_list
# %%
readme = pd.read_excel("readme.xlsx")
with pd.ExcelWriter('./test_results.xlsx') as writer:
    readme.to_excel(writer, sheet_name="readme",index=False)
    # 各データフレームを異なるシートとして保存
    for f,df in df_list:
        df.to_excel(writer, sheet_name=f.replace(".csv",""))

# %%
