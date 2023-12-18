# %%

import pandas as pd
import json

def get_data_from_excel(path:str,subjects:int = 17,iloc:int=9,index_col=None):
    return pd.read_excel(path,sheet_name=0,index_col=index_col)[:subjects].iloc[:,:iloc]

# %%

if __name__ == "__main__":
    with open('settings.json') as f:
        settings = json.load(f)
        dataset_dir = settings['dataset_dir']
    df = get_data_from_excel(f"{dataset_dir}/evals/test_model/acc_d2_results.xlsx")
    print(df)