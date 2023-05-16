import numpy as np

class SignalManager:
    def __init__(self, num_channels:int,sample_size=250):
        self.num_channels = num_channels
        self.sample_size = sample_size
        self.combined_data = np.empty((num_channels + 2, 0)) #信号チャンネル + 試行番目(-1=待機) + 正解クラス 
        self.saved_samples = []

    def add_signal(self,trial_num:int, signals:np.ndarray,true_class:int):
        if signals.shape[0] != self.num_channels:
            raise ValueError("Invalid signal shape")
        trial_num_row = np.full(signals.shape[1],trial_num)
        true_class_row = np.full(signals.shape[1],true_class)
        data = np.vstack([signals,trial_num_row,true_class_row])
        self.combined_data = np.hstack([self.combined_data, data])

    def get_last_samples(self):
        # 結合された信号の長さがサンプル数未満の場合はNoneを返す
        if self.combined_data.shape[1] < self.sample_size:
            return None

        last_samples = self.combined_data[:, -self.sample_size:]
        return last_samples

class PredictHistory():
    def __init__(self):
        self.history = []
    
    def add_data(self,trial_num:int,data:np.ndarray,predict_class:int):
        self.history.append((trial_num,data,predict_class))
