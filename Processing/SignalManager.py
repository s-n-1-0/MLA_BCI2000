import numpy as np

class SignalManager:
    def __init__(self, num_channels:int,sample_size=500):
        self.num_channels = num_channels
        self.sample_size = sample_size
        self.saved_samples = []
        self.total_combined_data = np.empty((self.num_channels + 2, 0))
        self.combined_data = np.empty((self.num_channels + 2, 0)) #信号チャンネル + 試行番目(-1=待機) + 正解クラス 

    def add_signal(self,trial_num:int, signals:np.ndarray,true_class:int):
        if signals.shape[0] != self.num_channels:
            raise ValueError("Invalid signal shape")
        trial_num_row = np.full(signals.shape[1],trial_num)
        true_class_row = np.full(signals.shape[1],true_class)
        data = np.vstack([signals,trial_num_row,true_class_row])
        self.combined_data = np.hstack([self.combined_data, data])
        self.total_combined_data = np.hstack([self.total_combined_data, data])

    def get_last_samples(self):
        # 結合された信号の長さがサンプル数未満の場合はNoneを返す
        if self.combined_data.shape[1] < self.sample_size:
            return None

        last_samples = self.combined_data[:, -self.sample_size:]
        return last_samples
    
    def reset(self):
        self.combined_data = np.empty((self.num_channels + 2, 0))
    
    def get_prev_true_class(self):
        if self.total_combined_data.shape == (self.num_channels+2,0):
            return 0
        return self.total_combined_data[-1,-1]
