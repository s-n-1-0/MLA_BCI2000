#
# NOTE: セッション合算のグラフ
#
# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math
import numpy as np
from matplotlib.patches import Rectangle
import json
from sklearn.linear_model import LinearRegression
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
from calculation_diffs import calc_diffs, merge_sessions
from scipy.stats import spearmanr
with open('../settings.json') as f:
    settings = json.load(f)
    dataset_dir = settings["dataset_dir"]
subject_laps_erders = [np.load("s1_erders.npy"),np.load("s2_erders.npy")]
subject_laps_acc_df = [get_data_from_excel(url).iloc[:,1:] for url in [
    f"{dataset_dir}/s1/evals/_acc_d2_results.xlsx",
    f"{dataset_dir}/s2/_evals/acc_d2_results.xlsx"
]]
subjects = [13,3]
print(subject_laps_acc_df[0])
print(subject_laps_acc_df[1])

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
def subject2index(lap:int,subject:int):
    if lap == 1:
        return subject - 1
    else:
        if subject < 5:
            return subject - 1
        elif subject < 14:
            return subject - 2
        return subject - 3

assert subject2index(2,17) == 14
assert subject2index(2,1) == 0
assert subject2index(2,7) == 5
# %%
_colors_keys = sorted(
            list(mcolors.CSS4_COLORS.keys()), key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))[15:]
colors_keys = np.array(_colors_keys)[[6,13,23,38,47,\
                           50,54,63,65,71,\
                            81,90,92,105,112,\
                                121,130]]
colors = {}
for key in colors_keys: colors[key] = mcolors.CSS4_COLORS[key]
def plot_colortable(colors, *, ncols=4, sort_colors=True):

    cell_width = 300
    cell_height = 22
    swatch_width = 48
    margin = 12

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        names = sorted(
            colors, key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))
    else:
        names = list(colors)

    n = len(names)
    nrows = math.ceil(n / ncols)

    width = cell_width * ncols + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * ncols)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, f"{i+1} {name} / {colors[name]}", fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=colors[name], edgecolor='0.7')
        )

    return fig
plot_colortable(colors, ncols=3, sort_colors=False)
colors = [colors[key] for key in colors_keys]
# %% ERD/ERSのプロット
def plot_erders(ch_erders,std,trials,title:str):
    fig = plt.figure(figsize=(7,10))
    for ch,ch_name in enumerate(["C3","Cz","C4"]):
        print(f"=>{ch}")
        for i,label in enumerate(["left","right"]):
            erders = ch_erders[ch,i]
            print(f"{label} : {len(erders)}")
            std_erders = std[ch,i] / np.sqrt(trials[ch,i])
            time_stft = np.linspace(0, 4, len(erders), endpoint=False)
            plt.subplot(3, 1, ch+1)
            plt.title(ch_name)
            plt.plot(time_stft, erders *100, label=label,color= "r" if "left" == label else "c")
            plt.plot(time_stft, (erders + std_erders) *100, linestyle="dotted",color= "r" if "left" == label else "c")
            plt.plot(time_stft, (erders - std_erders) *100, linestyle="dotted",color= "r" if "left" == label else "c")
            plt.plot(time_stft,[0]*len(time_stft),color="gray")
            if ch == 0:
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.xlabel("Time [s]")
            plt.ylabel("ERD/ERS [%] (M±SEM)")
            plt.ylim(-150,150)
    plt.suptitle(title)#: day{day}")#/FBNone {'First' if fb == 's1' else 'END'}")
    fig.tight_layout()
    plt.show()
for lap,subject_erders in zip([1,2],subject_laps_erders):
    for i,subject in zip([subject2index(lap,s) for s in subjects],subjects):
        print(f"{subject}人目({i})")
        for day in [0,3]:
            sessions,std,sm_sum = merge_sessions(subject_erders,
                                            i,day)
            plot_erders(sessions,
                        std,
                        sm_sum,
                        title=f"Subject {subject} /{lap}st / day{day+1} / pre+post"
                        )

# %% ERD/ERS DIFF プロット
def draw_bar(ch_diffs:np.ndarray,title:str):
    print(title)
    sems = np.std(ch_diffs,axis=1)/np.sqrt(ch_diffs.shape[1])
    plt.figure(figsize=(4,5))
    plt.bar(["C3","Cz","C4"], np.mean(ch_diffs,axis=1), width=0.6, yerr=sems, capsize=10,color=["r","gray","c"])
    plt.ylim([-1,1])
    plt.xlabel("Channels")
    plt.ylabel("Ch_Diff")
    plt.title(title)
    plt.show()
for lap,subject_erders in zip([1,2],subject_laps_erders):
    subject_diffs,subject_merged_diffs,subject_diffdiffs,subject_merged_diffdiffs = calc_diffs(subject_erders)
    for i,subject in zip([subject2index(lap,s) for s in subjects],subjects):
        day_diffs = subject_diffs[i]
        for day in [0,3]:
            draw_bar(subject_merged_diffs[i,day],
                    title=f"Subject {subject} /{lap}st / day{day+1} / pre+post (M+SEM)")

# %% C3-C4 DIFFDiff プロット
subject_nums = [1,2,3,4,5,7,8,9,10,11,12,13,15,16,17]
subject_indexes = [subject2index(lap,s) for s in subject_nums]
def draw_group_bar_scatter(lap:int,subject_acc_df,get_data_func,title:str):
    #散布図
    plt.figure()
    sx = get_data_func(slice(None)).reshape(-1,1)[subject_indexes]
    sy = (subject_acc_df.values[subject_indexes,day*2] + subject_acc_df.values[subject_indexes,day*2+1])/2
    for i,subject in enumerate(subject_nums):
        plt.scatter([sx[i]],[sy[i]],
                    color=colors[subject - 1 ],
                    label= f"{subject}")
    plt.xlim([-0.5,1.5])
    plt.ylim([0.4,1])
    mod = LinearRegression()
    mod_lin = mod.fit(sx,np.array(sy))
    y_lin_fit = mod_lin.predict(sx)
    r,p = spearmanr(sx[:,0],sy)
    r2 = r ** 2
    plt.text(0.5, 0.5, '$ R_s $=' + str(round(r,4)) + ',$ R_s^{2} $=' + str(round(r2, 4)) + "\n"+\
                "$ p_s $="+str(round(p,5)))
    plt.plot(sx, y_lin_fit, color = '#000000', linewidth=0.5)
    plt.title(title)
    plt.ylabel("Accuracy")
    plt.xlabel("Diff")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()

for lap,subject_erders,subject_acc_df in zip([1,2],subject_laps_erders,subject_laps_acc_df):
    subject_diffs,subject_merged_diffs,subject_diffdiffs,subject_merged_diffdiffs = calc_diffs(subject_erders)   
    for day in [0,3]:
        draw_group_bar_scatter(lap,subject_acc_df,lambda subject:subject_merged_diffdiffs[subject,day],
                    title=f"{lap}st / Day {day + 1} / pre+post")
# %% C3-C4 DIFF Rs
plt.figure()
rlist = []
for lap,subject_erders,subject_acc_df in zip([1,2],subject_laps_erders,subject_laps_acc_df):
    subject_diffs,subject_merged_diffs,subject_diffdiffs,subject_merged_diffdiffs = calc_diffs(subject_erders)
    #散布図
    diffdiffs = subject_merged_diffdiffs
    for day in range(diffdiffs.shape[1]):
        sx = diffdiffs[subject_indexes,day].reshape(-1,1)
        sy = (subject_acc_df.values[subject_indexes,day*2] + subject_acc_df.values[subject_indexes,day*2+1])/2
        rlist.append(spearmanr(sx,sy))
plt.plot(range(1,9),[r for r,_ in rlist],marker="8")
for i,_p in enumerate(rlist):
    r,p = _p
    if p < 0.05:
        plt.text(i+1,r+0.05,"*",ha='center')
plt.ylabel("$R_s$")
plt.title(f"Spearman's correlation coefficient")
plt.ylim([0,1])
xticks = []
xtick_labels = []
for x in range(1,9):
    xticks.append(x)
    xtick_labels.append(f"Day{(x-1) % 4 + 1}")
xticks.append(2.5)
xtick_labels.append("\n1st")
xticks.append(6.5)
xtick_labels.append("\n2st")
plt.xticks(xticks,xtick_labels)
xticks = plt.gca().xaxis.get_major_ticks()
for i,label in enumerate(xtick_labels):
    if label in ["\n1st","\n2st"]:
        xticks[i].tick1line.set_visible(False)
plt.show()
# %% C3-C4 DIFF 時系列
a_groups = [3,5,8,10,11,12,16,17]
b_groups = [1,2,4,7,9,13,15]
a_means = []
b_means = []
plt.figure()
for lap,subject_erders in zip([1,2],subject_laps_erders):
    subject_diffs,subject_merged_diffs,subject_diffdiffs,subject_merged_diffdiffs = calc_diffs(subject_erders)
    #散布図
    diffdiffs = subject_merged_diffdiffs
    
    for day in range(diffdiffs.shape[1]):
        _a_means = []
        _b_means = []
        for gi,group in enumerate([a_groups,b_groups]):
            for i,subject in zip([subject2index(lap,s) for s in group],group):
                offset = (-1 if gi == 0 else 1) * 0.1
                plt.scatter([day + (4*(lap-1))+offset],[diffdiffs[i,day]],
                            color=colors[subject - 1],
                            label= f"{subject}" if lap == 1 and day == 0 else "")
                if gi == 0:
                    _a_means.append(diffdiffs[i,day])
                else:
                    _b_means.append(diffdiffs[i,day])
        a_means.append(np.mean(_a_means))
        b_means.append(np.mean(_b_means))

plt.title(f"")
plt.plot(range(8),a_means,"8-",label="Cl1")
plt.plot(range(8),b_means,"8-",label="Cl2")

xticks = []
xtick_labels = []
for x in range(0,8):
    xticks.append(x-0.2)
    xticks.append(x+0.2)
    xticks.append(x)
    xtick_labels.append("Cl1")
    xtick_labels.append("Cl2")
    xtick_labels.append(f"\nDay{(x) % 4 + 1}")
xticks.append(1.5)
xtick_labels.append("\n\n1st")
xticks.append(5.5)
xtick_labels.append("\n\n2st")
plt.xticks(xticks,xtick_labels)
xticks = plt.gca().xaxis.get_major_ticks()
for i,label in enumerate(xtick_labels):
    if label in ["Cl1","Cl2","\n\n1st","\n\n2st"]:
        xticks[i].tick1line.set_visible(False)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.ylabel("Diff")
plt.title("Diff Transition")
#plt.minorticks_on()
plt.show()
# %%
