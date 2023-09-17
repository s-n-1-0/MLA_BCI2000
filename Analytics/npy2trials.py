# %%
import numpy as np
from scipy import stats
data_path = "C:/MLA_Saves/1/d1s1m1_data_2023_08_23_11_19_29_concatenate.npy"
fs = 500
# %%
full_data = np.load(data_path)
predictclass_list = []
trueclass_list = []
stim_data_list = []
for i in range(full_data.shape[0]):
    data = full_data[i,:,:]
    _trueclass_list = data[-3,:]
    true_flags = list((_trueclass_list == 1) | (_trueclass_list == 2))
    trueclass_list.append(int(_trueclass_list[true_flags][0]))
    si = true_flags.index(True)
    ei = true_flags[::-1].index(True)
    #plt.plot(range(len(x[si:-ei])),x[si:-ei])
    stim_data = data[:,si:-ei-1]
    stim_data_list.append(stim_data[:,:fs*4 - 50])
    #予測クラスの取得
    predict_counts = stim_data[-2,:]
    predict_count_indexes = []
    prev_pc = -1
    for j in range(len(predict_counts)):
        pc = predict_counts[j]
        if prev_pc != pc:
            prev_pc = pc
            if pc > 0:
                k = 1
                while j+k < len(predict_counts) and predict_counts[j+k] == pc:k+=1
                k -= 1
                #print((pc,predict_counts[j+k],k))
                predict_count_indexes.append((j,j+k))

    #print(predict_count_indexes)
    def pick_predictclass(pci,end):
        x = stim_data[-1,pci:end+1]
        mode = stats.mode(x,keepdims=True)[0]
        if mode == 0:
            for f in x:
                if f != 0:
                    return f
        return mode
    #カウントアップと同時に予測フラグが立つわけではないので最頻値で求める
    _predictclass_list = [int(pick_predictclass(pci[0],pci[1])) for pci in predict_count_indexes]
    predictclass_list.append(_predictclass_list)
stim_data = np.array(stim_data_list)
stim_data.shape

# %%
predictclass_list