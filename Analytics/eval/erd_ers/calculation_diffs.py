#
# ERD/ERSの差分を求める
#
import numpy as np

def merge_sessions(_subject_orders: np.ndarray, subject: int, day: int):
    # 各セッションの平均値、標準偏差、トライアル数を取得
    subject_means = _subject_orders[subject, day, :, :, :, 0, :]  # 平均値
    subject_std = _subject_orders[subject, day, :, :, :, 1, :]    # 標準偏差
    subject_trials = _subject_orders[subject, day, :, :, :, 2, :]  # トライアル数

    combined_mean = np.zeros(subject_means.shape[1:])
    combined_std_dev = np.zeros(subject_std.shape[1:])
    total_trials = np.zeros(subject_trials.shape[1:-1])

    # タイムスタンプごとに計算
    for ch in range(subject_means.shape[1]):
        for lr in range(subject_means.shape[2]):
            for ts in range(subject_means.shape[3]):
                # 重み付き平均値の計算
                weighted_mean_sum = np.sum(subject_means[:, ch, lr, ts] * subject_trials[:, ch, lr, 0])
                trial_sum = np.sum(subject_trials[:, ch, lr, 0])
                combined_mean[ch, lr, ts] = weighted_mean_sum / trial_sum

                # 標準偏差の結合
                var_sum = np.sum(subject_std[:, ch, lr, ts]**2 * subject_trials[:, ch, lr, 0])
                combined_std_dev[ch, lr, ts] = np.sqrt(var_sum / trial_sum)

                total_trials[ch, lr] = trial_sum

    return combined_mean, combined_std_dev, total_trials



def calc_ch_diffs(ch_data):
    ch_diffs = []
    for ch in range(ch_data.shape[0]):
        ch_diff = ch_data[ch,0]-ch_data[ch,1]
        ch_diffs.append(ch_diff)
    return  np.array(ch_diffs)
def calc_diffs(subject_erders:np.ndarray):
    subject_diffs = []
    subject_merged_diffs = []
    subject_diffdiffs = []
    subject_merged_diffdiffs = []
    for subject in range(subject_erders.shape[0]):
        day_erders = subject_erders[subject,:,:,:,:,0,:]
        day_diffs = []
        day_merged_diffs = []
        day_diffdiffs = []
        day_merged_diffdiffs = []
        for day in range(day_erders.shape[0]):
            session_diffs = []
            session_diffdiffs = []
            for session in range(day_erders.shape[1]):
                print(day+1,session+1)
                ch_diffs = calc_ch_diffs(day_erders[day,session])
                session_diffs.append(ch_diffs)
                session_diffdiffs.append(np.mean(ch_diffs[0] - ch_diffs[1]))
            day_diffs.append(session_diffs)
            data, _,_ = merge_sessions(subject_erders,
                                     subject,day)
            merged_ch_diff = calc_ch_diffs(data)
            day_merged_diffs.append(merged_ch_diff)
            day_diffdiffs.append(session_diffdiffs)
            day_merged_diffdiffs.append(np.mean(merged_ch_diff[0]-merged_ch_diff[1]))
        subject_diffs.append(day_diffs)
        subject_merged_diffs.append(day_merged_diffs)
        subject_diffdiffs.append(day_diffdiffs)
        subject_merged_diffdiffs.append(day_merged_diffdiffs)
    subject_diffs = np.array(subject_diffs)
    subject_merged_diffs = np.array(subject_merged_diffs)
    subject_diffdiffs = np.array(subject_diffdiffs)
    subject_merged_diffdiffs = np.array(subject_merged_diffdiffs)
    return (subject_diffs,subject_merged_diffs,
            subject_diffdiffs,subject_merged_diffdiffs)