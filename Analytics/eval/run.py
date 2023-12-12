# %%
import glob
import os
import papermill as pm
import json
with open('settings.json') as f:
    settings = json.load(f)
    dataset_dir = settings["dataset_dir"]
    lap_id = settings["lap_id"]
working_dir = f"{dataset_dir}/{lap_id}"
def generate_notebook(subject,day):
    subject_day_dir = f"{working_dir}/{subject}/{day}"
    file_paths = [f for f in glob.glob(subject_day_dir + "/*") if f.endswith(".npy") ]
    file_names = [os.path.split(f)[1][:-4] for f in file_paths]
    #d1_model_path = "C:/MLA Models/d1_model.h5"
    #d2_model_path = "C:/MLA Models/d2_model.h5"
    d3_model_path = "C:/MLA Models/d3_model.h5"
    for data_path,name in zip(file_paths,file_names):
        name = name.replace("_concatenate","")
        eval_dir = f"{working_dir}/evals/{subject}/{day}"
        if not os.path.exists(eval_dir):
            os.makedirs(eval_dir)
        pm.execute_notebook(
        "eval_template.ipynb",
        f"{eval_dir}/{name}.ipynb",
        parameters=dict(data_path=data_path,
                        sub_model_path=d3_model_path,
                        eval_dir=f"{working_dir}/evals"
                        )
        )
subjects = settings["subjects"]

_day = settings["day"]
run_all = settings["run_all"]
if run_all:
    subjects = [f for f in os.listdir(working_dir) if os.path.isdir(os.path.join(working_dir, f))]
    for s in subjects:
        #ignore
        if s in ["0000","1000","1001","1002"]:continue
        days = [f for f in os.listdir(working_dir+"/"+s) if os.path.isdir(os.path.join(working_dir+"/"+s, f))]
        for d in days:
            generate_notebook(s,d)
else:
    for subject in subjects:
        generate_notebook(subject,_day)
# %%
