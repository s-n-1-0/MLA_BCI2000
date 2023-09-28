# %%
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.signal import butter, filtfilt
from train_code.generator.raw_generator import transpose_raw2d
import keras
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath('__file__')), '..'))
from npy2trials import load_data
#TODO: この二つの関数は冗長
def preprocess(data,fs):
    #print(f"{scaler.mean_} / {scaler.scale_}")
    # バンドパスフィルタを適用
    if True:
        # バンドパスフィルタの設定
        lowcut = 8  # バンドパスフィルタの下限周波数
        highcut = 30  # バンドパスフィルタの上限周波数
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(2, [low, high], btype='band')
        data = filtfilt(b, a, data)

    # データを標準化
    scaler = StandardScaler()
    data = scaler.fit_transform(data.T).T
    return np.array(data)
def specificity(y_true, y_pred): pass

def eval_sequence(data:np.ndarray,fs:int,block_size:int,step:int,transpose_func,model):
    dataset = np.array([preprocess(data[:,ei-block_size:ei],fs) for ei in range(block_size,data.shape[1],step)])
    dataset = transpose_func(0,dataset)
    return [2 if p > 0.5 else 1 for p in model.predict(dataset,verbose = 0)]

    
def predict(model_path:str,loaded_data:np.ndarray,fs:int,ch_size:int,block_size:int,step:int):
    stim_data = loaded_data
    d1_model = keras.models.load_model(model_path,custom_objects={"specificity":specificity})
    all_data = stim_data[:,:ch_size,:]
    predictclass_list = []
    for i in range(all_data.shape[0]):
        predictclass_list.append(eval_sequence(all_data[i,:,:],fs,block_size,step,transpose_raw2d,d1_model))
    return predictclass_list

# %%
