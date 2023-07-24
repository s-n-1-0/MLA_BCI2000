import logging
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.signal import butter, filtfilt, periodogram


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
    # パワースペクトルへの変換
    #freq, data = periodogram(data, fs=fs)
    #"""
    #freq_range = [5, 20]  # 使用する周波数範囲
    # 特定の周波数範囲以内のインデックスを取得
    #in_range_idx = np.logical_and(freq >= freq_range[0], freq <= freq_range[1])
    # 特定の周波数範囲以内の特徴を残す
    #data = data[:, in_range_idx]
    #"""
    # 圧縮
    #new_data = []
    #for i in range(0, data.shape[0],20):
    #    new_data.append(np.mean(data[i:i+chunk_size], axis=0))
    return np.array(data)