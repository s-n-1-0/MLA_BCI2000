# %%
import numpy as np
import matplotlib.pyplot as plt
subject_erders = np.load("erders.npy")
subject_trials =  np.load("erders_trials.npy")
subject_erders.shape,subject_trials.shape#,subject_ignores.shape #日,セッション,ch,lr
# %%　人ごとのERD/ERSスコアを出力
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
                ch_data = np.mean(day_erders[day,session,ch,:],axis=1)
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
# %% ERD/ERS DIFF
subject_diffs = []
for subject in range(subject_erders.shape[0]):
    day_erders = subject_erders[subject]
    day_trials = subject_trials[subject]
    print(f"{subject +1}人目")
    day_diffs = []
    for day in range(day_erders.shape[0]):
        session_diffs = []
        for session in range(day_erders.shape[1]):
            print(day+1,session+1)
            ch_diffs = []
            for ch in range(day_erders.shape[2]):
                ch_data = day_erders[day,session,ch,:]
                #ch_size = np.sum(day_trials[day,session,ch])
                ch_diff = ch_data[0]-ch_data[1]
                ch_diffs.append(ch_diff)
            session_diffs.append(ch_diffs)
        day_diffs.append(session_diffs)
    subject_diffs.append(day_diffs)
        
    print("")
subject_diffs = np.array(subject_diffs)
print(np.array(subject_diffs).shape)
# %% ERD/ERS DIFF プロット
for subject in range(subject_diffs.shape[0]):
    day_diffs = subject_diffs[subject]
    print(f"{subject +1}人目")
    for day in range(day_diffs.shape[0]):
        session_diffs = []
        for session in range(day_diffs.shape[1]):
            print(day+1,session+1)
            ch_diffs = day_diffs[day,session,:,:]
            sems = np.std(ch_diffs,axis=1)/np.sqrt(ch_diffs.shape[1])
            plt.bar(["C3","Cz","C4"], np.mean(ch_diffs,axis=1), width=0.6, yerr=sems, capsize=10,color=["r","gray","c"])
            plt.title(f"Subject {subject + 1} / Session{session + 1} (M+SEM)")
            plt.show()
        

