# %%
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.signal import butter, filtfilt
from train_code.generator.raw_generator import transpose_raw2d
import keras
#TODO: この二つの関数は冗長
def preprocess(data,fs):
    #print(f"{scaler.mean_} / {scaler.scale_}")
    # バンドパスフィルタを適用
    if True:
        # バンドパスフィルタの設定
        lowcut = 8  # バンドパスフィルタの下限周波数
        highcut = 30  # バンドパスフィルタの上限周波数
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(2, [low, high], btype='band')
        data = filtfilt(b, a, data)

    # データを標準化
    scaler = StandardScaler()
    data = scaler.fit_transform(data.T).T
    return np.array(data)
def specificity(y_true, y_pred): pass

def eval_sequence(data:np.ndarray,fs:int,block_size:int,step:int,transpose_func,model):
    dataset = np.array([preprocess(data[:,ei-block_size:ei],fs) for ei in range(block_size,data.shape[1],step)])
    dataset = transpose_func(0,dataset)
    return [2 if p > 0.5 else 1 for p in model.predict(dataset,verbose = 0)]

    
def predict(model_path:str,loaded_data:np.ndarray,fs:int,ch_size:int,block_size:int,step:int):
    stim_data = loaded_data
    d1_model = keras.models.load_model(model_path,custom_objects={"specificity":specificity})
    all_data = stim_data[:,:ch_size,:]
    predictclass_list = []
    for i in range(all_data.shape[0]):
        predictclass_list.append(eval_sequence(all_data[i,:,:],fs,block_size,step,transpose_raw2d,d1_model))
    return predictclass_list

# %% #任意のモデルで結果を出力
# TODO: 要整理
if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath('__file__')), '..'))
    from npy2trials import load_data
    import glob
    import os
    import json
    import csv
    from analyse1 import analyse1
    
    """
    オプション
    """
    model_path = ""
    fs = 500
    ch_size = 13
    block_size = 750
    step = 250


    with open('settings.json') as f:
        settings = json.load(f)
        dataset_dir = settings['dataset_dir']
        lap_id = settings["lap_id"]
    target_dir = f"{dataset_dir}/{lap_id}"
    def write_metrics(subject,day):
        subject_day_dir = f"{target_dir}/{subject}/{day}"
        file_paths = [f for f in glob.glob(subject_day_dir + "/*") if f.endswith(".npy") ]
        file_names = [os.path.split(f)[1][:-4] for f in file_paths]
        
        for data_path,name in zip(file_paths,file_names):
            name = name.replace("_concatenate","")
            eval_dir = f"{target_dir}/evals"
            if not os.path.exists(eval_dir):
                os.makedirs(eval_dir)
            x = np.load(data_path)
            stim_data,predictclass_list,trueclasses = load_data(x,fs)
            if model_path != "":
                predictclass_list = predict(model_path,stim_data,fs,ch_size,block_size,step)
            else:
                print("モデルパスが未指定のためデータに保存されている予測値を使用。")
            data_metrics,data_detailed_metrics,_ = analyse1(trueclasses,predictclass_list)
            for d0,apname in zip([data_metrics,data_detailed_metrics],
                            ["","_detailed"]):
                log_path = eval_dir + "/output_acc" + apname + ".csv"
                with open(log_path, 'a') as f:
                    writer = csv.writer(f, lineterminator='\n') # 行末は改行
                    nlst = data_path.replace(dataset_dir+"/","").replace("\\","/").split("/")[1:]
                    cols = [nlst[0],nlst[1],nlst[2]]
                    cols += [d0[0][0],d0[1][0]] ##accだけ追加
                    writer.writerow(cols)
                    
            for d0,apname in zip([data_metrics,data_detailed_metrics],
                            ["","_detailed"]):
                log_path = eval_dir + "/output_ex" + apname + ".csv"
                with open(log_path, 'a') as f:
                    writer = csv.writer(f, lineterminator='\n') # 行末は改行
                    nlst = data_path.replace(dataset_dir+"/","").replace("\\","/").split("/")[1:]
                    cols = [nlst[0],nlst[1],nlst[2]]
                    for i in range(1,3):
                        cols += [d0[0][i],d0[1][i]]#つまり通常とfixed
                        cols += ["/"] #評価関数が変わったら / 列挿入
                    writer.writerow(cols)
    subjects = [f for f in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, f))]
    for s in subjects:
        #ignore
        if s in ["0000","1000","1001","1002"]:continue
        days = [f for f in os.listdir(target_dir+"/"+s) if os.path.isdir(os.path.join(target_dir+"/"+s, f))]
        for d in days:
            write_metrics(s,d)

# %%
