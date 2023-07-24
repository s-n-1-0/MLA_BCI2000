import datetime
import os
import numpy as np

class SignalManager:
    def __init__(self,settings, num_channels:int,sample_size=750):
        now = datetime.datetime.now()
        dir_name = f"{settings['save_path']}/{settings['subject_id']}/data_{now.strftime('%Y_%m_%d_%H_%M_%S')}"
        if not os.path.exists(dir_name):
             os.makedirs(dir_name)
        self.dir_name = dir_name
        self.num_channels = num_channels
        self.sample_size = sample_size
        self.saved_samples = []
        self.total_combined_data = np.empty((self.num_channels + 4, 0))
        self.reset_stim() #信号チャンネル + 試行番目(-1=待機) + 正解クラス

    def add_signal(self,trial_num:int,
                   signals:np.ndarray,
                   true_class:int,
                   predict_count:int,
                   predict_class:int):
        if signals.shape[0] != self.num_channels:
            raise ValueError("Invalid signal shape")
        trial_num_row = np.full(signals.shape[1],trial_num)
        true_class_row = np.full(signals.shape[1],true_class)
        predict_count_row = np.full(signals.shape[1],predict_count)
        predict_class_row = np.full(signals.shape[1],predict_class)
        data = np.vstack([signals,trial_num_row,true_class_row,predict_count_row,predict_class_row])
        if true_class > 0:
            self.combined_data = np.hstack([self.combined_data, data])
        self.total_combined_data = np.hstack([self.total_combined_data, data])
    def get_last_samples(self):
        # 結合された信号の長さがサンプル数未満の場合はNoneを返す
        if self.combined_data.shape[1] < self.sample_size:
            return None

        last_samples = self.combined_data[:, -self.sample_size:]
        return last_samples
    
    def reset_and_save(self):
        if self.combined_data.shape[1] ==  0:
            return
        trial_num = self.combined_data[-4,-1]
        dir_name = self.dir_name
        np.save(f"{dir_name}/{int(trial_num)}", self.total_combined_data)
        self.reset_stim()
        self.total_combined_data = np.empty((self.num_channels + 4, 0))
    def reset_stim(self):
        self.combined_data = np.empty((self.num_channels + 4, 0))