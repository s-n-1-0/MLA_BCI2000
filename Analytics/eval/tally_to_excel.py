#
# 全ての結果を集計してエクセルにまとめます。
#
# %%
import json
import pandas as pd
import numpy as np
with open('settings.json') as f:
    settings = json.load(f)
    dataset_dir = settings['dataset_dir']
    session_id = settings["session_id"]
    toe_settings = settings["tally_to_excel"]

    source_file = toe_settings["source_file"]
    target_file_name = toe_settings["target_file_name"]
    target_indexes = toe_settings["target_indexes"]
    target_sheet_names = toe_settings["target_sheet_names"]

file_keys = ["s1m1","s1m2","s2","s3","s4m1","s4m2"]
isalignment = True #FB有りを除いて整列 
# %%
working_path = dataset_dir + "/" + session_id
source_path = working_path + toe_settings["relative_source_dir"] + "/" + source_file
acc_data = pd.read_csv(source_path,header=None).values

#
# 変換される辞書は
#   subject:
#      day:[key,日付,以降csvごとの列データ]
def convert_data2dict(data):
    d = {}
    for i in range(data.shape[0]):
        subject = data[i,0]
        day = data[i,1]
        if subject not in d:
            d[subject] = {}
        subject_dict = d[subject]
        if day not in subject_dict:
            subject_dict[day] = []
        subject_dict[day].append(data[i,2:])
    for subject in d:
        subject_dict = d[subject]
        for day in subject_dict:
            #不足があればエラー
            assert len(subject_dict[day]) ==  len(file_keys),subject_dict[day]
            #並び替え
            old_sessions = subject_dict[day]
            sorted_sessions = [None]*len(file_keys)
            for s in old_sessions:
                file_name = s[0].split("_")[0][2:]
                file_date = "-".join(s[0].split("_")[2:-1])
                i = file_keys.index(file_name)
                sorted_sessions[i] = list(s)
                sorted_sessions[i][0] = file_name
                sorted_sessions[i].insert(1,file_date)
            assert None not in sorted_sessions,str(subject) + str(sorted_sessions) #適切に並び替えできているかどうか
            subject_dict[day] = sorted_sessions
    return d
acc_dict = convert_data2dict(acc_data)
acc_dict
# %% シート作成

#ファイル名の次の列を0番目とカウント
if isalignment:
    heads_headers = ["参加者番号"]
    tails_headers = [f"{i+1}日目FB無{j+1}" for i in range(4) for j in range(2)]
else:
    heads_headers = ["参加者番号","〇日目"]
    tails_headers = ["無し1-1","無し1-2","無し1平均","","有り1","有り2","有り平均","","無し2-1","無し2-2","無し2平均",""]
def make_df(headers:list,d,data_colnum,offset = 2):
    new_data = []
    subjects = sorted(d.keys())
    for subject in subjects:
        subject_dict = acc_dict[subject]
        days = sorted(subject_dict.keys())
        if not isalignment: #通常(FB有りも出力)
            for day in days:
                #セッションは既に変換時ソート済みなのでそのまま利用できる
                _row_data = [d[offset+data_colnum] if not np.isnan(d[offset+data_colnum]) else d[offset+data_colnum-1] for d in subject_dict[day]]
                row_data = []
                for i in range(0,6,2):
                    row_data.append(_row_data[i])
                    row_data.append(_row_data[i+1])
                    row_data.append(np.mean([_row_data[i],_row_data[i+1]]))
                    row_data.append("")
                new_data.append([subject,day]+row_data)
        else:
            row_data = []
            for day in days:
                #セッションは既に変換時ソート済みなのでそのまま利用できる
                _row_data = [d[offset+data_colnum] if not np.isnan(d[offset+data_colnum]) or data_colnum == 0 else d[offset+data_colnum-1] for d in subject_dict[day]]
                for i in [0,4]:
                    row_data.append(np.mean([_row_data[i],_row_data[i+1]]))
            new_data.append([subject]+row_data)
    df = pd.DataFrame(new_data, columns =headers)
    return df

df_list = [ make_df(heads_headers+tails_headers,acc_dict,i) for i in target_indexes]#if acc_data.shape[1] == 6 else 3)

# %%一列目をヘッダー、2列目を値にしたDataFrameを作成
line_df_list = [] #一列目をヘッダー、2列目を値にした行列のリスト(被験者番号は情報欠損する)
for df in df_list:
    new_data = []
    for column in df.columns:
        if column in heads_headers: #基本ヘッダーの場合はスキップ
            continue
        new_data +=  [[column,value] for value in (df[column].values)]
    line_df_list.append(pd.DataFrame(new_data,columns=None))

# %% Excelに保存
with pd.ExcelWriter(f"{working_path}/evals/{target_file_name}_results.xlsx") as writer:
        for sheet_name,df,lf,ti in zip(target_sheet_names,df_list,line_df_list,target_indexes):
            df.to_excel(writer, sheet_name=f"{sheet_name} col{ti}",index=False)
            lf.to_excel(writer, sheet_name=f"{sheet_name} col{ti}_line",index=False,header=False)
# %%
