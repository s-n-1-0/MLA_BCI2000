import numpy as np

import numpy as np

class SignalManager:
    def __init__(self, num_channels,sample_size=250):
        self.num_channels = num_channels
        self.sample_size = sample_size
        self.signals = np.empty((num_channels, 0))
        self.saved_samples = []

    def add_signal(self, signals):
        if signals.shape[0] != self.num_channels:
            raise ValueError("Invalid combined signal shape")
        self.signals = np.hstack([self.signals, signals])

    def get_last_samples(self, value):
        combined_signal = self.signals

        # 結合された信号の長さがサンプル数未満の場合はNoneを返す
        if combined_signal.shape[1] < self.sample_size:
            return None

        last_samples = combined_signal[:, -self.sample_size:]
        self.saved_samples.append((value, last_samples))
        return last_samples

    def get_saved_samples(self):
        return self.saved_samples