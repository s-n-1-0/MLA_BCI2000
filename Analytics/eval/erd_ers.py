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
import io
from PIL import Image
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

isplot = True #プロット表示するかどうか
isfirst_baseline = True #開始時の待機時間をベースラインとするかどうか
iseach_day = False
len(ch_indexes),ch_indexes

with open('./settings.json') as f:
    settings = json.load(f)
    h5_path = settings["h5_path"]

# %%
def fig_to_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    return img
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
def show_errorbar(left_erders,right_erders,left_err,right_err):
    from matplotlib.transforms import ScaledTranslation
    import matplotlib as mpl
    mpl.rcParams['axes.xmargin'] = 0.1
    x = ["C3","Cz","C4"]
    fig = plt.figure(figsize=(4, 7))
    ax = plt.subplot()
    trans1 = ax.transData + ScaledTranslation(-5/72, 0, fig.dpi_scale_trans)
    trans2 = ax.transData + ScaledTranslation(+5/72, 0, fig.dpi_scale_trans)
    ax.errorbar(x, left_erders*100, yerr=left_err*100, marker="o",color="r", linestyle="none", transform=trans1)
    ax.errorbar(x, right_erders*100, yerr=right_err*100, marker="o",color="c" ,linestyle="none", transform=trans2)
    ax.set_ylim(-150,150)
    img = fig_to_img(fig)
    fig.suptitle(f"ERD/ERS")
    plt.show()
    return img
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
        stim = stim[:,:1950] #厳密に4秒ではなくて右端の0.1秒は捨てる(調整用)
        if label == "left":
            stims_left.append(stim)
            baselines_left.append(baseline)
            key_left.append(key)
        else:
            stims_right.append(stim)
            baselines_right.append(baseline)
            key_right.append(key)
    print(len(stims_left),len(stims_right))

    fig = plt.figure(figsize=(10, 7))
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
            erders = np.mean(erders,axis=0)
            lr_erders.append(np.mean(erders))
            lr_err.append(np.mean(std_erders))
            
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
                plt.plot(time_stft, (erders + std_erders) *100, linestyle="dotted",color= "r" if "left" == label else "c")
                plt.plot(time_stft, (erders - std_erders) *100, linestyle="dotted",color= "r" if "left" == label else "c")
                plt.plot(time_stft,[0]*len(time_stft),color="gray")
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.xlabel("Time [s]")
                plt.ylabel("ERD/ERS")
                plt.ylim(-250,250)
        ignore_count_list.append(iglist)
        ch_erders.append(lr_erders)
        ch_err.append(lr_err)
    if isplot:
        plt.suptitle(f"subject {subject} ")#: day{day}")#/FBNone {'First' if fb == 's1' else 'END'}")
        erders_img = fig_to_img(fig)
        err_img = show_errorbar(np.array(ch_erders)[:,0],np.array(ch_erders)[:,1],np.array(ch_err)[:,0],np.array(ch_err)[:,1])
        total_width = erders_img.width + err_img.width
        max_height = max(erders_img.height, err_img.height)
        new_img = Image.new('RGB', (total_width, max_height), (255, 255, 255))
        new_img.paste(erders_img, (0, 0))
        new_img.paste(err_img, (erders_img.width, 0))

        # 結合した画像を保存または表示
        #new_img.show()
        erders_img.close()
        err_img.close()
        new_img.save(f"./figs/{subject}.png")
    return ch_erders,ignore_count_list
# %%
first_dict = get_first_fixs_erders()

# %%
subject_erders = []
subject_ignores = []
for subject in range(1,18):
    day_erders = []
    day_ignores = []
    print(subject)
    if iseach_day:
        for day in range(1,5):
            session_erders = []
            session_ignores = []
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
subject_erders = np.array(subject_erders)
subject_ignores = np.array(subject_ignores)
np.save("erders.npy",subject_erders)
np.save("erders_ignores.npy",subject_ignores)
subject_erders.shape,subject_ignores.shape #日,セッション,ch,lr
# %%
stests = []
for subject in range(subject_erders.shape[0]):
    day_erders = subject_erders[subject]
    stests.append(0)
    print(f"{subject +1}人目")
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
                stests[subject] += 1
            else:
                print("通過")
    print("")
print(stests)