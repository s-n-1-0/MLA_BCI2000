# %%
import glob
import os
import papermill as pm
import json
with open('settings.json') as f:
    settings = json.load(f)
subject = settings["subject"]
subject_dir = f"{settings['dataset_dir']}/{subject}"
# %%
file_paths = [f for f in glob.glob(subject_dir + "/*") if f.endswith(".npy") ]
file_names = [os.path.split(f)[1][:-4] for f in file_paths]
file_names
# %%
for data_path,name in zip(file_paths,file_names):
    name = name.replace("_concatenate","")
    eval_dir = f"{settings['dataset_dir']}/evals/{subject}"
    if not os.path.exists(eval_dir):
        os.makedirs(eval_dir)
    pm.execute_notebook(
    "eval.ipynb",
    f"{eval_dir}/{name}.ipynb",
    parameters=dict(data_path=data_path)
    )