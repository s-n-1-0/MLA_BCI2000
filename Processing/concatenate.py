
#このファイルを出力データファイルがあるフォルダに配置して実行することで、データを連結したファイルが親フォルダに生成されます。
#生成ファイル名は"フォルダ名_concatenate.npy"
# %%
import os
import numpy as np
data_files = [d for d in os.listdir() if ".npy" == d[-4:]]

data_list = []
for df in data_files:
    data = np.load(df)
    data_list.append(data)

min_size = np.min([d.shape[1] for d in data_list])
resized_data = np.array([d[:,-min_size:] for d in data_list])
current_directory = os.path.basename(os.getcwd())
np.save(f"../{current_directory}_concatenate",resized_data)