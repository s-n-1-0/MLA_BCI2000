#
# ERD/ERSの差分を求める
#
import numpy as np
def merge_sessions(_subject_erders:np.ndarray,
            subject:int,
            day:int):
    subject_erders = _subject_erders[:,:,:,:,:,0,:]
    subject_trials = _subject_erders[:,:,:,:,:,2,0]
    ts_product = subject_erders[subject,day] * subject_trials[subject,day][..., np.newaxis]
    ts_sum = np.sum(ts_product, axis=0)  # sessionに関する次元で合計
    # subject_trialsについて、必要な次元に沿って合計を計算
    sm_sum = np.sum(subject_trials[subject,day], axis=0)
    sessions = ts_sum / sm_sum[..., np.newaxis]
    return sessions,sm_sum
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
            data, _ = merge_sessions(subject_erders,
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