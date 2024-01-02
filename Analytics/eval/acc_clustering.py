# %%
import json
import matplotlib.pyplot as plt
import numpy as np
from tslearn.clustering import TimeSeriesKMeans
from load_excel import get_data_from_excel
with open('settings.json') as f:
    settings = json.load(f)
    lap_id = settings["lap_id"]
    dataset_dir = settings["dataset_dir"] + "/" + lap_id

n = 3
subjects = 15
is_centering = False
metric = "euclidean"
excel_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
subject_acc_df = get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0)
print(subject_acc_df)
nm_data = subject_acc_df.values#TimeSeriesScalerMeanVariance().fit_transform(subject_acc_df.values)
print(nm_data.shape)
if is_centering:
    nm_data = nm_data - np.nanmean(nm_data,axis=1,keepdims=True)
    print(nm_data.mean(axis=1,keepdims=True).shape)
sse_list = [] 
for i in range(1,subjects): 
    ts_km = TimeSeriesKMeans(n_clusters=i, random_state=1234, metric=metric,max_iter=1000)
    ts_km.fit_predict(nm_data)
    sse_list.append(ts_km.inertia_) 

plt.plot(range(1,subjects),sse_list,marker="o") 
plt.xticks(range(1,subjects)) 
plt.xlabel("Number of clusters") 
plt.ylabel("SSE") 
plt.show()

km = TimeSeriesKMeans(n_clusters=n, random_state=1234, metric=metric,max_iter=1000)
labels = km.fit_predict(nm_data)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
fig, axes = plt.subplots(n, figsize=(8.0, 18.0))
plt.subplots_adjust(hspace=0.5)
for i in range(n):
    ax = axes[i]
    for xx in nm_data[labels == i]:
        ax.plot(xx.ravel(), "k-", alpha=.2)
    ax.plot(km.cluster_centers_[i].ravel(), "r-")
    
    nm_ymin, nm_ymax = (0.4,1)
    ax.set_ylim(nm_ymin, nm_ymax)
    plt.xlabel("   ")
    plt.ylabel("   ")
    ax.set_xticks(range(16))
    datanum = np.count_nonzero(labels == i)
    ax.text(0.5, (nm_ymax*0.9+nm_ymin*0.1), f'Cluster {(i + 1)} : n = {datanum} ({",".join([str(l) for l in subject_acc_df.index[labels == i]])})')
    if i == 0:
        ax.set_title(metric.capitalize() + " k-means")
# %%
