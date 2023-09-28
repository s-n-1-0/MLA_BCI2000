#
# ERD/ERSを出力するコード(要調整・要整理)
#
# %%
import h5py
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import filtfilt
from typing import Callable
fs = 500
subject =13
# %%

eeglist = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10', 'FC3', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3', 'CPz', 'CP4', 'P1', 'P2', 'POz', 'FT9', 'FTT9h', 'TTP7h', 'TP7', 'TPP9h', 'FT10', 'FTT10h', 'TPP8h', 'TP8', 'TPP10h', 'F9', 'F10', 'AF7', 'AF3', 'AF4', 'AF8', 'PO3', 'PO4']
using_lst = ['FC5','FC1','FC2','FC6','C3','C1','Cz','C2','C4','CP5','CP1','CP2','CP6']
using_lst = ['C3','Cz','C4']
ch_indexes = []
for item in using_lst:
    ch_indexes.append(eeglist.index(item))
ch_indexes = [4,6,8] #NOTE:MLA.h5用
len(ch_indexes),ch_indexes

with open('./eval/settings.json') as f:
    settings = json.load(f)
    h5_path = settings["h5_path"]
# %%
def get_trials(dataset_filter:Callable[[h5py.Dataset],bool]):
    with h5py.File(h5_path) as h5:
        count = h5["origin"].attrs["count"]
        labels = []
        baselines = []
        stims = []
        for i in range(count):
            dataset = h5[f"origin/{i}"]
            attrs = dataset.attrs
            stim_start = 1000
            stim_start = attrs["stim_index"]
            if not dataset_filter(dataset):
                continue
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
            baselines.append(data[ch_indexes,stim_start-400:stim_start])
            assert stim_start-400 >= 0,stim_start
            stims.append(data[ch_indexes,stim_start:])
    return labels,stims,baselines
def stft(x, fftsize=1024, overlap=4):
    hop = fftsize // overlap
    w = np.hanning(fftsize)
    return np.array([np.fft.fft(w*(x[i:i+fftsize])) for i in range(0, len(x) - fftsize, hop)])
def stft_and_filt(_time,data):
    time = np.linspace(0, _time, int(_time*fs), endpoint=False)
    fftsize = 256
    res_data = []
    for ch in range(3):
        ch_data =  data[ch,:len(time)]
        # Compute STFT
        overlap = 4
        stft_data = np.abs(stft(ch_data, fftsize, overlap))**2
        # Select frequencies between 8 and 30 Hz
        freqs = np.fft.fftfreq(fftsize, 1/fs)
        selected_freqs = (freqs >= 8) & (freqs <= 30)
        # Average over selected frequencies
        res_data.append(np.mean(stft_data[:, selected_freqs], axis=1))
    return np.array(res_data)
def get_erders(dataset_filter:Callable[[h5py.Dataset],bool],isplot = False):
    T = 4  # Duration in seconds
    labels,stims,baselines = get_trials(dataset_filter)     
    # STFT function
    baselines_left = []
    baselines_right = []
    stims_left = []
    stims_right = []
    for label,baseline,stim in zip(labels,baselines,stims):
        stim = stim[:,:1950]
        if label == "left":
            stims_left.append(stim)
            baselines_left.append(baseline)
        else:
            stims_right.append(stim)
            baselines_right.append(baseline)
    print(len(stims_left),len(stims_right))

    plt.figure(figsize=(10, 7))
    ch_erders = []
    for ch,ch_name in enumerate(["C3","Cz","C4"]):
        lr_erders = []
        for label,_stims,_baselines in zip(["left","right"],[stims_left,stims_right],[baselines_left,baselines_right]):
            erders = []
            for stim,baseline in zip(_stims,_baselines):
                stft_stim = stft_and_filt(T,stim)[ch,:]
                stft_baseline = stft_and_filt(T,baseline)[ch,:]
                b = np.mean(stft_baseline)
                e = (stft_stim - b)/b
                #print(b)
                if np.max(e) < 50:
                    erders.append(e)
            erders = np.array(erders)
            erders = np.mean(erders,axis=0)
            lr_erders.append(np.mean(erders))
            if isplot:
                # Time vector for STFT
                time_stft = np.linspace(0, T, len(erders), endpoint=False)
                plt.subplot(3, 1, ch+1)
                plt.title(ch_name)
                #plt.plot(time_stft, baseline_avg, label="Baseline")
                #for e in erders:
                #    time_stft = np.linspace(0, T, len(e), endpoint=False) #TODO: 後で消す
                #    plt.plot(time_stft, e *100, label=label)
                plt.plot(time_stft, erders *100, label=label,color= "r" if "left" == label else "c")
                plt.plot(time_stft,[np.mean(erders)*100]*len(time_stft),linestyle = "dashed",color= "r" if "left" == label else "c")
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xlabel("Time [s]")
                plt.ylabel("ERD/ERS")
                plt.ylim(-200,200)
        ch_erders.append(lr_erders)
    return ch_erders
day_erders = []
for day in range(1,5):
    session_erders = []
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
            #"""
            if f"d{day}" not in attrs["mla_key"]:
                ret = False
            if attrs["stim_index"]-500 < 0:
                ret = False
            return ret
        erders = get_erders(dataset_filter,isplot=True)
        session_erders.append(erders)
        plt.suptitle(f"subject {subject} : day{day}/FBX {'First' if fb == 's1' else 'END'}")
        plt.show()
    day_erders.append(session_erders)

# %%
day_erders = np.array(day_erders)
np.save("test.npy",day_erders)
day_erders.shape #日,セッション,ch,lr
# %%
for day in range(day_erders.shape[0]):
    for session in range(day_erders.shape[1]):
        print(day+1,session+1)
        c3=0
        c4=0
        for ch in range(day_erders.shape[2]):
            ch_data = day_erders[day,session,ch,:]
            if ch == 0:
                c3 = ch_data[1]-ch_data[0]
                print(ch,c3)
            elif ch == 2:
                c4 = ch_data[0]-ch_data[1]
                print(ch,c4)
        if c3 > 0 or c4 > 0 or np.abs(c3) > 2 or np.abs(c4) > 2:
            print("除外")
        else:
            print("通過")

# %%
