# %%
import glob
import os
import json
import numpy as np
from npy2trials import load_data
from eeghdf import EEGHDFUpdater
fs = 500
with open('./eval/settings.json') as f:
    settings = json.load(f)
    dataset_dir = settings['dataset_dir']
    h5_path = settings["h5_path"]
updater = EEGHDFUpdater(h5_path,fs,lables=["left","right"])
updater.remove_hdf()
def build_hdf(subject,day):
    subject_day_dir = f"{settings['dataset_dir']}/{subject}/{day}"
    file_paths = [f for f in glob.glob(subject_day_dir + "/*") if f.endswith(".npy") ]
    file_names = [os.path.split(f)[1][:-4] for f in file_paths]
    for data_path,name in zip(file_paths,file_names):
        name = name.replace("_concatenate","")
        if "s2" in name or "s3" in name: continue #FB有りを除外
        data,_,flag_list = load_data(np.load(data_path),fs)
        data  = data[:,:13,:] #使わないチャンネルを削除
        for i,flag in enumerate(["left" if flag == 1 else "right" for flag in flag_list]):
            updater.add_numpy(data[i,:,:],[0],[flag],data.shape[2],
                              dataset_attrs={"subject":int(subject),
                                            "session":day,
                                            "mla_key":name.split("_")[0]})
subjects = [f for f in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, f))]
for s in subjects:
    #ignore
    if s in ["0000","1000","1001","1002","sample"]:continue
    days = [f for f in os.listdir(dataset_dir+"/"+s) if os.path.isdir(os.path.join(dataset_dir+"/"+s, f))]
    for d in days:
        build_hdf(s,d)
