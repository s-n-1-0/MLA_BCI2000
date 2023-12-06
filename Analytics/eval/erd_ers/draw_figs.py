# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import os
from PIL import Image
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

# %% ERD/ERSのプロット
def fig_to_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    return img
def show_errorbar(left_erders,right_erders,left_err,right_err):
    from matplotlib.transforms import ScaledTranslation
    import matplotlib as mpl
    mpl.rcParams['axes.xmargin'] = 0.1
    x = ["C3","Cz","C4"]
    fig = plt.figure(figsize=(3, 7))
    ax = plt.subplot()
    trans1 = ax.transData + ScaledTranslation(-5/72, 0, fig.dpi_scale_trans)
    trans2 = ax.transData + ScaledTranslation(+5/72, 0, fig.dpi_scale_trans)
    ax.errorbar(x, left_erders*100, yerr=left_err*100, marker="o",color="r", linestyle="none", transform=trans1)
    ax.errorbar(x, right_erders*100, yerr=right_err*100, marker="o",color="c" ,linestyle="none", transform=trans2)
    ax.set_ylim(-150,150)
    img = fig_to_img(fig)
    fig.suptitle(f"ERD/ERS (M+SEM)")
    plt.show()
    return img
for subject in range(subject_erders.shape[0]):
    print(f"{subject +1}人目")
    for day in range(day_erders.shape[0]):
        for session in range(day_erders.shape[1]):
            fig = plt.figure(figsize=(10, 7))
            ch_erders = subject_erders[subject,day,session]
            ch_err = np.std(ch_erders,axis=2)/np.sqrt(subject_trials[subject,day,session])
            ch_mean = np.mean(ch_erders,axis=2)
            for ch,ch_name in enumerate(["C3","Cz","C4"]):
                print(f"=>{ch}")
                for i,label in enumerate(["left","right"]):
                    erders = subject_erders[subject,day,session,ch,i]
                    print(f"{label} : {len(erders)}")
                    std_erders = np.std(erders,axis=0)
                    time_stft = np.linspace(0, 4, len(erders), endpoint=False)
                    plt.subplot(3, 1, ch+1)
                    plt.title(ch_name)
                    plt.plot(time_stft, erders *100, label=label,color= "r" if "left" == label else "c")
                    plt.plot(time_stft, (erders + std_erders) *100, linestyle="dotted",color= "r" if "left" == label else "c")
                    plt.plot(time_stft, (erders - std_erders) *100, linestyle="dotted",color= "r" if "left" == label else "c")
                    plt.plot(time_stft,[0]*len(time_stft),color="gray")
                    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                    plt.xlabel("Time [s]")
                    plt.ylabel("ERD/ERS")
                    plt.ylim(-150,150)
            plt.suptitle(f"subject {subject+1} / day{day+1} / session{session+1}")#: day{day}")#/FBNone {'First' if fb == 's1' else 'END'}")
            erders_img = fig_to_img(fig)
            err_img = show_errorbar(ch_mean[:,0],ch_mean[:,1],ch_err[:,0],ch_err[:,1])
            total_width = erders_img.width + err_img.width
            max_height = max(erders_img.height, err_img.height)
            new_img = Image.new('RGB', (total_width, max_height), (255, 255, 255))
            new_img.paste(erders_img, (0, 0))
            new_img.paste(err_img, (erders_img.width, 0))

            # 結合した画像を保存または表示
            #new_img.show()
            erders_img.close()
            err_img.close()
            dir_path = f"./figs/erders/{subject+1}"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            new_img.save(f"{dir_path}/{day+1}_{session+1}.png")
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
        for session in range(day_diffs.shape[1]):
            print(day+1,session+1)
            ch_diffs = day_diffs[day,session,:,:]
            sems = np.std(ch_diffs,axis=1)/np.sqrt(ch_diffs.shape[1])
            plt.bar(["C3","Cz","C4"], np.mean(ch_diffs,axis=1), width=0.6, yerr=sems, capsize=10,color=["r","gray","c"])
            plt.ylim([-1,1])
            plt.title(f"Subject {subject + 1} / Day{day+1} / Session{session + 1} (M+SEM)")
            plt.show()

# %% ERD/ERS DIFF の集団プロット
width = 0.25
margin = 0.2
block = width * subject_diffs.shape[0] + margin
colors = list(mcolors.TABLEAU_COLORS.keys()) + \
         list(mcolors.CSS4_COLORS.keys())[15:]#15番以降
for day in range(subject_diffs.shape[1]):
    for session in range(subject_diffs.shape[2]):
        ind = np.arange(3) * block
        plt.figure(figsize=(10, 7))
        for subject in range(subject_diffs.shape[0]):
            day_diffs = subject_diffs[subject]
            ch_diffs = day_diffs[day,session,:,:]
            sems = np.std(ch_diffs,axis=1)/np.sqrt(ch_diffs.shape[1])
            plt.bar(
                ind + width*subject,
                np.mean(ch_diffs,axis=1),
                width,
                yerr=sems,
                color=colors[subject],
                label= f"{subject+1}"
                )
        plt.ylim([-1.25,1.25])
        plt.title(f"Day {day + 1} / Session{session + 1} (M+SEM)")
        xlabels = ["C3", "Cz", "C4"]
        xlocs = ind + width * 17 / 2.
        plt.xticks(xlocs, xlabels )
        plt.xlim(-margin, ind[-1]+width*subject_diffs.shape[0]+margin)
        plt.legend(prop={'size' : 18},loc='upper left', bbox_to_anchor=(1, 1))
        plt.show()