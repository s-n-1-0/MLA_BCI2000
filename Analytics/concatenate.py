
#このファイルを出力データファイルがあるフォルダの親に配置して実行することで、データを連結したファイルが生成されます。
#生成ファイル名は"フォルダ名_concatenate.npy"
# %%
import os
import numpy as np
from natsort import natsorted
dirs = [
    f for f in os.listdir() if os.path.isdir(os.path.join("./", f))
]
for dir in dirs:
    data_files = [d for d in os.listdir(dir) if ".npy" == d[-4:]]
    data_files = natsorted(data_files)
    data_list = []
    for df in data_files:
        data = np.load(f"{dir}/{df}")
        data_list.append(data)

    min_size = np.min([d.shape[1] for d in data_list])
    resized_data = np.array([d[:,-min_size:] for d in data_list])
    np.save(f"{dir}_concatenate",resized_data)
# %%
