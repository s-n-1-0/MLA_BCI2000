#
# ERD/ERSを出力するコード(要調整・要整理)
#
# %%
import eeghdf
import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.signal import hilbert,filtfilt
fs = 500
subject =5
# %%
#updater = eeghdf.EEGHDFUpdater("test.h5",fs=500,lables=["left","right"])
#updater.remove_hdf()
#updater.add_eeglab(".mat.set")
# %%
import h5py
eeglist = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6', 'T7', 'C3', 'Cz', 'C4', 'T8', 'TP9', 'CP5', 'CP1', 'CP2', 'CP6', 'TP10', 'P7', 'P3', 'Pz', 'P4', 'P8', 'PO9', 'O1', 'Oz', 'O2', 'PO10', 'FC3', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3', 'CPz', 'CP4', 'P1', 'P2', 'POz', 'FT9', 'FTT9h', 'TTP7h', 'TP7', 'TPP9h', 'FT10', 'FTT10h', 'TPP8h', 'TP8', 'TPP10h', 'F9', 'F10', 'AF7', 'AF3', 'AF4', 'AF8', 'PO3', 'PO4']
using_lst = ['FC5','FC1','FC2','FC6','C3','C1','Cz','C2','C4','CP5','CP1','CP2','CP6']
using_lst = ['C3','Cz','C4']
ch_indexes = []
for item in using_lst:
    ch_indexes.append(eeglist.index(item))
ch_indexes = [4,6,8]
len(ch_indexes),ch_indexes
# %%
def moving_variance(signal, N):
    valid_length = len(signal) - N + 1  # 有効な分散を計算できるポイントの数
    if valid_length <= 0:
        raise ValueError("Window size must be less than or equal to the signal length.")
    
    variances = np.zeros(valid_length)  # 有効なポイントのみを保存するための配列を初期化
    for i in range(valid_length):
        window = signal[i:i + N]  # ウィンドウサイズ分のデータを抽出
        variances[i] = np.var(window)  # ウィンドウ内の分散を計算
    return variances
    

for day in range(1,5):
    for fb in ["s1","s4"]:
        with open('./eval/settings.json') as f:
            settings = json.load(f)
            h5_path = settings["h5_path"]
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
                if fb not in attrs["mla_key"]:
                    continue

                #フィルター
                #"""
                if attrs["subject"] != subject:
                    continue
                #"""
                if f"d{day}" not in attrs["mla_key"]:
                    continue
                
                if attrs["stim_index"]-500 < 0:
                    continue
                labels.append(attrs["label"])
                #print(np.max(dataset[()]),np.min(dataset[()]))
                data = []#StandardScaler().fit_transform(dataset[()].T).T + 750
                d = dataset[()]
                for i in range(d.shape[0]):
                    N = 100  # フィルタの窓サイズ
                    b = np.ones(N)/N
                    a = 1
                    x = d[i,:] - filtfilt(b, a, d[i,:]) #移動平均フィルタ
                    #x = moving_variance(x,50)
                    data.append(x)
                    #plt.plot(range(len(d[i,:])),(min_max(d[i,:] - filtfilt(b, a, d[i,:]))*200-100)/5)
                    #plt.show()
                data = np.array(data)#StandardScaler().fit_transform(np.array(data).T).T + 750
                baselines.append(data[ch_indexes,attrs["stim_index"]-400:attrs["stim_index"]])
                assert attrs["stim_index"]-400 >= 0,attrs["stim_index"]
                stims.append(data[ch_indexes,attrs["stim_index"]:])
        fftsize = 256
        T = 4  # Duration in seconds
        time = np.linspace(0, T, int(T*fs), endpoint=False)
        # STFT function
        def stft(x, fftsize=1024, overlap=4):
            hop = fftsize // overlap
            w = np.hanning(fftsize)
            return np.array([np.fft.fft(w*(x[i:i+fftsize])) for i in range(0, len(x) - fftsize, hop)])
        def stft_filt(data):
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
        i = 0
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
        for ch,ch_name in enumerate(["C3","Cz","C4"]):
            for label,_stims,_baselines in zip(["left","right"],[stims_left,stims_right],[baselines_left,baselines_right]):
                erders = []
                for stim,baseline in zip(_stims,_baselines):
                    stft_stim = stft_filt(stim)[ch,:]
                    stft_baseline = stft_filt(baseline)[ch,:]
                    b = np.mean(stft_baseline)
                    e = (stft_stim - b)/b
                    #print(b)
                    if np.max(e) < 50:
                        erders.append(e)
                    else:
                        print(ch,np.max(e))
                erders = np.array(erders)
                erders = np.mean(erders,axis=0)
                # Time vector for STFT
                time_stft = np.linspace(0, T, len(erders), endpoint=False)


                plt.subplot(3, 1, ch+1)
                plt.title(ch_name)
                #plt.plot(time_stft, baseline_avg, label="Baseline")
                #for e in erders:
                #    time_stft = np.linspace(0, T, len(e), endpoint=False) #TODO: 後で消す
                #    plt.plot(time_stft, e *100, label=label)
                plt.plot(time_stft, erders *100, label=label)
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xlabel("Time [s]")
                plt.ylabel("ERD/ERS")
                plt.ylim(-200,200)
        plt.suptitle(f"subject {subject} : day{day}/FBX {'First' if fb == 's1' else 'END'}")
        plt.show()

# %%
time_stft.shape
# %%
