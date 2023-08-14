# %%
import glob
import os
import papermill as pm
import json
with open('settings.json') as f:
    settings = json.load(f)
subject = settings["subject"]
day = settings["day"]
subject_day_dir = f"{settings['dataset_dir']}/{subject}/{day}"
# %%
file_paths = [f for f in glob.glob(subject_day_dir + "/*") if f.endswith(".npy") ]
file_names = [os.path.split(f)[1][:-4] for f in file_paths]
file_names
# %%
d1_model_path = "C:/MLA Models/d1_model.h5"
d2_model_path = "C:/MLA Models/d2_model.h5"
for data_path,name in zip(file_paths,file_names):
    name = name.replace("_concatenate","")
    eval_dir = f"{settings['dataset_dir']}/evals/{subject}/{day}"
    if not os.path.exists(eval_dir):
        os.makedirs(eval_dir)
    pm.execute_notebook(
    "eval.ipynb",
    f"{eval_dir}/{name}.ipynb",
    parameters=dict(data_path=data_path,d1_model_path=d1_model_path,d2_model_path=d2_model_path)
    )