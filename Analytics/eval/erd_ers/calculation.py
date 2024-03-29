#
# ERD/ERSを出力するコード(要調整・要整理)
# 
# データ除外条件
#   - MLA以外のデータは除去
#   - 抽出データのstim時間が1秒未満のものは除去
# プロット条件
#   + 日ごとに出力
#       + FB無1またはFB無4を対象に分析
#   + 
#
# %%
import h5py
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import filtfilt,butter, lfilter
from typing import Callable, Dict
from bci_dataset.hdf_controller import HDFController

fs = 500
# %%

"""
3Pデータセットの場合
eeglist = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10', 'FC3', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3', 'CPz', 'CP4', 'P1', 'P2', 'POz', 'FT9', 'FTT9h', 'TTP7h', 'TP7', 'TPP9h', 'FT10', 'FTT10h', 'TPP8h', 'TP8', 'TPP10h', 'F9', 'F10', 'AF7', 'AF3', 'AF4', 'AF8', 'PO3', 'PO4']
using_lst = ['FC5','FC1','FC2','FC6','C3','C1','Cz','C2','C4','CP5','CP1','CP2','CP6']
using_lst = ['C3','Cz','C4']
ch_indexes = []
for item in using_lst:
    ch_indexes.append(eeglist.index(item))
"""
ch_indexes = [4,6,8] #NOTE:MLA.h5用

isfirst_baseline = True #開始時の待機時間をベースラインとするかどうか
iseach_day = True
len(ch_indexes),ch_indexes

with open('../settings.json') as f:
    settings = json.load(f)
    h5_path = settings["h5_path"]
    lap_id = settings["lap_id"]

# %%
def make_first_dict_key(attrs:dict):
    return str(attrs["subject"]) + "_" + str(attrs["session"]) + "_" + attrs["mla_key"]
def get_trials(dataset_filter:Callable[[h5py.Dataset],bool]):
    """
    指定した条件を満たす試行のラベルと表示区間(stims)と待機区間(baselines)のデータを返す
    """
    with h5py.File(h5_path) as h5:
        count = h5["origin"].attrs["count"]
        labels = []
        baselines = []
        stims = []
        keys = []
        for i in range(count):
            dataset = h5[f"origin/{i}"]
            attrs = dataset.attrs
            stim_start = attrs["stim_index"]
            if not dataset_filter(dataset): #分析対象じゃなかったら飛ばす
                continue
            keys.append(make_first_dict_key(dataset.attrs))
            labels.append(attrs["label"])
            data = []
            d = dataset[()]
            for i in range(d.shape[0]):
                N = 100  # フィルタの窓サイズ
                b = np.ones(N)/N
                a = 1
                x = d[i,:] - filtfilt(b, a, d[i,:]) #移動平均フィルタ
                data.append(x)
            data = np.array(data)#StandardScaler().fit_transform(np.array(data).T).T + 750
            baselines.append(data[ch_indexes,stim_start-(1 if isfirst_baseline else 550):stim_start])
            if not isfirst_baseline: assert stim_start-550 >= 0,stim_start
            stims.append(data[ch_indexes,stim_start:])
    return labels,stims,baselines,keys
def stft(x, fftsize=1024, overlap=4):
    hop = fftsize // overlap
    w = np.hanning(fftsize)
    return np.array([np.fft.fft(w*(x[i:i+fftsize])) for i in range(0, len(x) - fftsize, hop)])
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = lfilter(b, a, data)
    return y
def stft_and_filt(timestamp_range:slice,data):
    fftsize = 256
    res_data = []
    for ch in range(3):
        ch_data = bandpass_filter(data[ch,timestamp_range],8,30,fs) 
        # Compute STFT
        overlap = 4
        stft_data = np.abs(stft(ch_data, fftsize, overlap))**2
        # Select frequencies between 8 and 30 Hz
        freqs = np.fft.fftfreq(fftsize, 1/fs)
        selected_freqs = (freqs >= 8) & (freqs <= 30)
        # Average over selected frequencies
        res_data.append(np.mean(stft_data[:, selected_freqs], axis=1))
    return np.array(res_data)

def get_first_fixs_erders():
    first_dict:Dict[str,np.ndarray] = {}
    for dataset in HDFController(h5_path).get_in_order("origin"):
        si = dataset.attrs["stim_index"]
        if  si > 5000:
            dkey = make_first_dict_key(dataset.attrs)
            d = dataset[()]
            data = []
            for i in range(d.shape[0]):
                N = 100  # フィルタの窓サイズ
                b = np.ones(N)/N
                a = 1
                x = d[i,:] - filtfilt(b, a, d[i,:]) #移動平均フィルタ
                data.append(x)
            data = np.array(data)
            first_dict[dkey] = data[ch_indexes,:si]
    first_erders_dict = {}
    for key in first_dict:
        data = first_dict[key]
        first_erders_dict[key] = [np.mean(stft_and_filt(slice(-fs*5,None),data)[i,:]) for i in range(3)]
    return first_erders_dict
def get_erders(subject:int,dataset_filter:Callable[[h5py.Dataset],bool]):
    T = 4  # Duration in seconds
    labels,stims,baselines,keys = get_trials(dataset_filter)     
    # STFT function
    baselines_left = []
    baselines_right = []
    stims_left = []
    stims_right = []
    key_left = []
    key_right = []
    for label,baseline,stim,key in zip(labels,baselines,stims,keys):
        stim = stim[:,:1990]
        assert stim.shape[1] == 1990,stim.shape
        if label == "left":
            stims_left.append(stim)
            baselines_left.append(baseline)
            key_left.append(key)
        else:
            stims_right.append(stim)
            baselines_right.append(baseline)
            key_right.append(key)
    print(len(stims_left),len(stims_right))

    ch_erders = []
    ch_err = []
    ignore_count_list = [] #ch×(lr,2)
    for ch,ch_name in enumerate(["C3","Cz","C4"]):
        print(f"=>{ch}")
        lr_erders = []
        lr_err = []
        iglist = [0,0,0,0,0] #%スレッシュホールド
        for label,_stims,_baselines,_keys in zip(["left","right"],
                                           [stims_left,stims_right],
                                           [baselines_left,baselines_right],
                                           [key_left,key_right]):
            erders = []
            for stim,baseline,key in zip(_stims,_baselines,_keys):
                stft_stim = stft_and_filt(slice(0,T*fs),stim)[ch,:]
                if isfirst_baseline:
                    b = first_dict[key][ch]
                else:
                    stft_baseline = stft_and_filt(slice(-550,None),baseline)[ch,:]
                    b = np.mean(stft_baseline)
                e = (stft_stim - b)/b #ERD/ERS式
                #print(b)
                max_erders = np.max(e)
                if max_erders < 10: #ERSが10倍(1000%)になっているなら除外する
                    erders.append(e)
                
                if max_erders >= 100:
                    iglist[-1] += 1
                if max_erders >= 50:
                    iglist[-2] += 1
                if max_erders >= 20:
                    iglist[-3] += 1
                if max_erders >= 10:
                    iglist[-4] += 1
                if max_erders >= 1:
                    iglist[-5] += 1
            print(f"{label} : {len(erders)}")
            erders = np.array(erders)
            std_erders = np.std(erders,axis=0)
            print(erders.shape)
            lr_erders.append([np.mean(erders,axis=0),
                              np.std(erders,axis=0),
                              [erders.shape[0]]*erders.shape[1]])
            lr_err.append(std_erders)
        ignore_count_list.append(iglist)
        ch_erders.append(lr_erders)
        ch_err.append(lr_err)#
    return ch_erders,ignore_count_list,
# %%
first_dict = get_first_fixs_erders()

# %%
subject_erders = []
subject_ignores = []
for subject in range(1,18) if lap_id == "s1" else [1,2,3,4,5,7,8,9,10,11,12,13,15,16,17]:
    day_erders = []
    day_ignores = []
    print(subject)
    if iseach_day:
        for day in range(1,5):
            session_erders = []
            session_ignores = []
            session_trials = []
            for fb in ["s1","s4"]:
                def dataset_filter(dataset:h5py.Dataset):
                    attrs = dataset.attrs
                    ret = True
                    if fb not in attrs["mla_key"]:   
                        ret = False
                    #フィルター
                    #"""
                    if attrs["subject"] != subject:
                        ret = False
                    
                    if f"d{day}" not in attrs["mla_key"]:
                        ret = False
                    if (not isfirst_baseline) and attrs["stim_index"]-550 < 0:
                        ret = False
                    return ret
                erders,ignore_list = get_erders(subject,dataset_filter)
                session_erders.append(erders)
                session_ignores.append(ignore_list)
            day_erders.append(session_erders)
            day_ignores.append(session_ignores)
    else:
        session_erders = []
        session_ignores = []
        def dataset_filter(dataset:h5py.Dataset):
            attrs = dataset.attrs
            ret = True
            for fb in ["s1","s4"]:
                if fb in attrs["mla_key"]:   
                    ret = True
                    break
                else:    
                    ret = False
            #フィルター
            #"""
            if attrs["subject"] != subject:
                ret = False
            
            #if f"d{day}" not in attrs["mla_key"]:
            #    ret = False
            if (not isfirst_baseline) and attrs["stim_index"]-550 < 0:
                ret = False
            return ret
        erders,ignore_list = get_erders(subject,dataset_filter)
        session_erders.append(erders)
        session_ignores.append(ignore_list)
        day_erders.append(session_erders)
        day_ignores.append(session_ignores)
    subject_erders.append(day_erders)
    subject_ignores.append(day_ignores)

# %%
np.save(lap_id + "_erders.npy",np.array(subject_erders))
np.save(lap_id + "_erders_ignores.npy",np.array(subject_ignores))
np.array(subject_erders).shape,np.array(subject_ignores).shape
# %%
