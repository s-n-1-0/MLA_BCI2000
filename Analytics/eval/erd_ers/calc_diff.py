# %%
import numpy as np
subject_erders = np.load(".erders.npy")
subject_erders.shape#,subject_ignores.shape #日,セッション,ch,lr
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