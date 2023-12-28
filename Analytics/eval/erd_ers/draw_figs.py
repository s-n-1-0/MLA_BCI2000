#
# NOTE: セッション合算のグラフ
#
# %%
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import os
import json
from PIL import Image
from sklearn.linear_model import LinearRegression
import sys
sys.path.append('../')
from load_excel import get_data_from_excel
from calculation_diffs import calc_diffs, merge_sessions
from scipy.stats import pearsonr,spearmanr
with open('../settings.json') as f:
    settings = json.load(f)
    lap_id = settings["lap_id"]
    dataset_dir = settings["dataset_dir"] + "/" + lap_id
subject_erders = np.load(lap_id + "_erders.npy")
subject_acc_df = get_data_from_excel(f"{dataset_dir}/evals/_acc_d2_results.xlsx").iloc[:,1:]
print(subject_acc_df)
subject_erders.shape#,subject_ignores.shape #日,セッション,ch,lr
# %%　人ごとのERD/ERSスコアを出力
stests = []
for subject in range(subject_erders.shape[0]):
    day_erders = subject_erders[subject,:,:,:,:,0]
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
def plot_save(ch_erders,trials,title:str,save_path:str):
    fig = plt.figure(figsize=(10, 7))
    ch_err = np.std(ch_erders,axis=2)/np.sqrt(trials)
    ch_mean = np.mean(ch_erders,axis=2)
    for ch,ch_name in enumerate(["C3","Cz","C4"]):
        print(f"=>{ch}")
        for i,label in enumerate(["left","right"]):
            erders = ch_erders[ch,i]
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
            plt.ylabel("ERD/ERS (M±SEM)")
            plt.ylim(-150,150)
    plt.suptitle(title)#: day{day}")#/FBNone {'First' if fb == 's1' else 'END'}")
    erders_img = fig_to_img(fig)
    err_img = show_errorbar(ch_mean[:,0],ch_mean[:,1],ch_err[:,0],ch_err[:,1])
    total_width = erders_img.width + err_img.width
    max_height = max(erders_img.height, err_img.height)
    new_img = Image.new('RGB', (total_width, max_height), (255, 255, 255))
    new_img.paste(erders_img, (0, 0))
    new_img.paste(err_img, (erders_img.width, 0))
    # 結合した画像を保存または表示
    erders_img.close()
    err_img.close()
    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    new_img.save(save_path)
for subject in range(subject_erders.shape[0]):
    print(f"{subject +1}人目")
    for day in range(day_erders.shape[0]):
        for session in range(day_erders.shape[1]):
            plot_save(subject_erders[subject,day,session,:,:,0,:],
                      subject_erders[subject,day,session,:,:,2,0],
                      title=f"subject {subject+1} / day{day+1} / session{session+1}",
                      save_path=f"./figs/erders/{subject+1}/{day+1}_{session+1}.png"
                      )
        sessions,sm_sum = merge_sessions(subject_erders,
                                         subject,day)
        plot_save(sessions,
                      sm_sum,
                      title=f"subject {subject+1} / day{day+1} / session 1+2",
                      save_path=f"./figs/erders/{subject+1}/{day+1}_1+2.png"
                      )
# %% ERD/ERS DIFF
subject_diffs,subject_merged_diffs,subject_diffdiffs,subject_merged_diffdiffs = calc_diffs(subject_erders)
subject_diffs.shape,subject_merged_diffs.shape,subject_diffdiffs.shape,subject_merged_diffdiffs.shape
# %% ERD/ERS DIFF プロット
def draw_bar(ch_diffs:np.ndarray,title:str,save_path:str):
    sems = np.std(ch_diffs,axis=1)/np.sqrt(ch_diffs.shape[1])
    plt.bar(["C3","Cz","C4"], np.mean(ch_diffs,axis=1), width=0.6, yerr=sems, capsize=10,color=["r","gray","c"])
    plt.ylim([-1,1])
    plt.title(title)
    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    plt.savefig(save_path)
    plt.show()
for subject in range(subject_diffs.shape[0]):
    day_diffs = subject_diffs[subject]
    print(f"{subject +1}人目")
    for day in range(day_diffs.shape[0]):
        for session in range(day_diffs.shape[1]):
            print(day+1,session+1)
            draw_bar(day_diffs[day,session,:,:],
                     title=f"Subject {subject + 1} / Day{day+1} / Session{session + 1} (M+SEM)",
                     save_path=f"./figs/diff/{subject+1}/{day+1}_{session+1}.png")
        draw_bar(subject_merged_diffs[subject,day],
                 title=f"Subject {subject + 1} / Day{day+1} / Session 1+2 (M+SEM)",
                 save_path=f"./figs/diff/{subject+1}/1+2.png")
print(subject_diffdiffs.shape)
# %% ERD/ERS DIFF の集団プロット
width = 0.25
margin = 0.2
block = width * subject_diffs.shape[0] + margin
colors = list(mcolors.TABLEAU_COLORS.keys()) + \
         list(mcolors.CSS4_COLORS.keys())[15:]#15番以降
ind = np.arange(3) * block
for day in range(subject_diffs.shape[1]):
    for session in range(subject_diffs.shape[2]):
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
        plt.savefig(f"./figs/diff/group_{day+1}_{session+1}.png")
        plt.show()
    #session 1+2
    plt.figure(figsize=(10, 7))
    for subject in range(subject_diffs.shape[0]):
        day_diffs = subject_merged_diffs[subject]
        ch_diffs = day_diffs[day,:,:]
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
    plt.title(f"Day {day + 1} / Session1+2 (M+SEM)")
    xlabels = ["C3", "Cz", "C4"]
    xlocs = ind + width * 17 / 2.
    plt.xticks(xlocs, xlabels )
    plt.xlim(-margin, ind[-1]+width*subject_diffs.shape[0]+margin)
    plt.legend(prop={'size' : 18},loc='upper left', bbox_to_anchor=(1, 1))
    plt.savefig(f"./figs/diff/group_{day+1}_1+2.png")
    plt.show()
# %% C3-C4 DIFF プロット

def draw_group_bar_scatter(get_data_func,title:str,save_path:str):
    width = 0.25
    margin = 0.2
    is_pearson = False #Flaseならスピアマン
    colors = list(mcolors.TABLEAU_COLORS.keys()) + \
            list(mcolors.CSS4_COLORS.keys())[15:]#15番以降
    plt.figure(figsize=(10, 7))
    for subject in range(subject_diffs.shape[0]):
        diff = get_data_func(subject)
        #sems = np.std(diff,axis=1)/np.sqrt(ch_diffs.shape[1])
        plt.bar(
            width*subject,
            diff,
            width,
            #yerr=sems,
            color=colors[subject],
            label= f"{subject+1}"
            )
    plt.ylim([-0.5,1.25])
    plt.title(f"Day {day + 1} / Session{session + 1}")
    plt.xlim(-margin, width*subject_diffs.shape[0]+margin)
    plt.legend(prop={'size' : 18},loc='upper left', bbox_to_anchor=(1, 1))
    dir_path = os.path.dirname(save_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    dlist = save_path.split("/")
    dlist[-1] = "bar_"  + dlist[-1]
    plt.savefig("/".join(dlist))
    plt.show()

    #散布図
    plt.figure(figsize=(10, 7))
    sx = get_data_func(slice(None)).reshape(-1,1)
    sy = subject_acc_df.values[:,day*2+session]
    for subject in range(subject_diffs.shape[0]):
        plt.scatter([sx[subject]],[sy[subject]],
                    color=colors[subject],
                    label= f"{subject+1}")
    plt.xlim([-0.5,1.5])
    plt.ylim([0,1])
    mod = LinearRegression()
    mod_lin = mod.fit(sx,np.array(sy))
    y_lin_fit = mod_lin.predict(sx)
    if is_pearson:
        r,p = pearsonr(sx[:,0],sy)
        r2 = r ** 2
        plt.text(0.5, 0.2, '$ R $=' + str(round(r,4)) + ',$ R^{2} $=' + str(round(r2, 4)) + "\n"+\
                 "$ p $="+str(round(p,5)))
    else:
        r,p = spearmanr(sx[:,0],sy)
        r2 = r ** 2
        plt.text(0.5, 0.2, '$ R_s $=' + str(round(r,4)) + ',$ R_s^{2} $=' + str(round(r2, 4)) + "\n"+\
                 "$ p_s $="+str(round(p,5)))
    plt.plot(sx, y_lin_fit, color = '#000000', linewidth=0.5)
    plt.title(title)
    plt.legend(prop={'size' : 18},loc='upper left', bbox_to_anchor=(1, 1))
    dlist = save_path.split("/")
    dlist[-1] = "scatter_"  + dlist[-1]
    plt.savefig("/".join(dlist))
    plt.show()
    
for day in range(subject_diffs.shape[1]):
    for session in range(subject_diffs.shape[2]):
        draw_group_bar_scatter(lambda subject:subject_diffdiffs[subject,day,session],
        title=f"Day {day + 1} / Session{session + 1}",
        save_path=f"./figs/diffdiff/{day+1}_{session+1}.png")
    draw_group_bar_scatter(lambda subject:subject_merged_diffdiffs[subject,day],
                 title=f"Day {day + 1} / Session 1+2",
                 save_path=f"./figs/diffdiff/{day+1}_1+2.png")
subject_diffdiffs.shape
# %%
import math
import numpy as np
from matplotlib.patches import Rectangle
_colors_keys = sorted(
            list(mcolors.CSS4_COLORS.keys()), key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))[15:]
colors_keys = np.array(_colors_keys)[[6,13,23,38,47,\
                           50,54,63,65,71,\
                            81,90,92,105,112,\
                                121,130]]
_colors = {}
#for key in mcolors.TABLEAU_COLORS.keys(): _colors[key] = mcolors.TABLEAU_COLORS[key]
for key in mcolors.CSS4_COLORS.keys(): _colors[key] = mcolors.CSS4_COLORS[key]
colors = {}
for key in colors_keys:
    colors[key] = _colors[key]
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
[colors[key] for key in colors_keys]
# %%
subject_erders[15,0,1,0,0,0,:]
# %%
