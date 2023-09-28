import numpy as np
from scipy import stats
from sklearn.metrics import confusion_matrix
def calculate_cm(tclasses,pclass_list):
    predictclass_mode_list = []
    matched_predict_count = 0
    for t,p in zip(tclasses,pclass_list):#total_acc算出 calculate
        assert len(p) > 0,p
        mode_predict = int(stats.mode(p,keepdims=True)[0])
        predictclass_mode_list.append(mode_predict)
        p_true = np.count_nonzero(np.array(p) == t)
        matched_predict_count += p_true
        #print(t,p_true)

    detailed_tclasses = []
    detailed_pclasses = []
    for i,pl in enumerate(pclass_list):
        detailed_tclasses += [tclasses[i]]*len(pl)
        detailed_pclasses += pl
    cm = confusion_matrix(tclasses, predictclass_mode_list)
    detailed_cm = confusion_matrix(detailed_tclasses, detailed_pclasses)
    return np.array(cm),detailed_cm,predictclass_mode_list
def calculate_metrics(cm):
    acc = (cm[0,0]+cm[1,1])/np.sum(cm)
    trsums = np.sum(cm,axis=1)
    recall = cm[0,0]/trsums[0]
    spec = cm[1,1]/trsums[1]
    return acc,recall,spec


def zip_metrics(trsums,metrics,fixed_metrics):
    if trsums[0] == trsums[1]: #クラス数に差がないなら修正しない
        return [metrics,[None]*len(fixed_metrics)]
    return [metrics,fixed_metrics]

def print_zipped_metrics(zipped):
    mtexts = ["精度","再現率(Recall)","特異度(Specificity)"]
    for i in range(2):
        text = ""
        if zipped[i][0] is not None:
            for mtext,metric in zip(mtexts,zipped[i]):
                text += f"{mtext} : {metric:.4f} "
            if i == 1:
                text += ":::補正:アンダーサンプリング"
            print(text)

def analyse1(trueclasses:list,predictclass_list:list[list]):
    cm,detailed_cm,predictclass_mode_list = calculate_cm(trueclasses, predictclass_list)
    metrics = calculate_metrics(cm)
    detailed_metrics = calculate_metrics(detailed_cm)
    std_list = []
    left_mean_list = []
    left_std_list = []
    right_mean_list = []
    right_std_list = []
    mn_predictclass_list = []

    #acc修正
    trsums = np.sum(cm,axis=1)
    minsum = np.min(trsums)
    lcount = rcount = 0
    fixed_trueclasses = []
    fixed_predictclass_list = []
    for i,y in enumerate(trueclasses):
        if y == 1:
            if lcount == minsum:
                continue
            lcount+=1
        else:
            if rcount == minsum:
                continue
            rcount+=1
        fixed_trueclasses.append(trueclasses[i])
        fixed_predictclass_list.append(predictclass_list[i]) 
    fixed_cm,fixed_detailed_cm,fixed_predictclass_mode_list = calculate_cm(fixed_trueclasses, fixed_predictclass_list)
    fixed_metrics = calculate_metrics(fixed_cm)
    fixed_detailed_metrics = calculate_metrics(fixed_detailed_cm)
    m = zip_metrics(trsums,metrics,fixed_metrics)
    dm = zip_metrics(trsums,detailed_metrics,fixed_detailed_metrics)
    print_zipped_metrics(m)
    # 混同行列を表示
    print("混同行列:")
    print(cm)
    
    if m[1][0] is not None:
        print("修正混同行列:")
        print(fixed_cm)
    
    print("----詳細評価----")
    print_zipped_metrics(dm)

    print("-------通常評価-------")
    print("　|真|判別シークエンス|最頻|〇/×|std|mean")
    for i,_pack in enumerate(zip(trueclasses,predictclass_list,predictclass_mode_list)):
        tl, pl,pml = _pack
        std = np.std(pl)
        mean = np.mean(pl)
        #if tl == 2:
        print(i+1,tl,pl,pml,"〇" if np.count_nonzero(np.array(pl) == tl) > len(pl)//2 else "×",std,mean)
        mn_predictclass_list.append([1 if tl == p else 0 for p in pl])
        std_list.append(std)
        if tl == 1:#1==left
            left_std_list.append(std)
            left_mean_list.append(mean)
        else:
            right_std_list.append(std)
            right_mean_list.append(mean)
    print(f"真が左の平均{np.mean(left_mean_list)} 標準偏差{np.mean(left_std_list)}")
    print(f"真が右の平均{np.mean(right_mean_list)} 標準偏差{np.mean(right_std_list)}")
    return m,dm,mn_predictclass_list