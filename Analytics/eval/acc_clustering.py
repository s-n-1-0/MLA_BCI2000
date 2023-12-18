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
subjects = 17
is_centering = False
metric = "dtw"
excel_path = "C:/Users/2221012/Downloads/1+2日目.xlsx"
subject_acc_df = get_data_from_excel(excel_path,subjects=subjects,iloc=17,index_col=0).iloc[:,1:]
print(subject_acc_df)
nm_data = subject_acc_df.values#TimeSeriesScalerMeanVariance().fit_transform(subject_acc_df.values)
print(nm_data.shape)
if is_centering:
    nm_data = nm_data - np.nanmean(nm_data,axis=1,keepdims=True)
    print(nm_data.mean(axis=1,keepdims=True).shape)
distortions = [] 
for i in range(1,subjects): 
    ts_km = TimeSeriesKMeans(n_clusters=i, random_state=1234, metric=metric,max_iter=1000)
    ts_km.fit_predict(nm_data)
    distortions.append(ts_km.inertia_) 

plt.plot(range(1,subjects),distortions,marker="o") 
plt.xticks(range(1,subjects)) 
plt.xlabel("Number of clusters") 
plt.ylabel("Distortion") 
plt.show()

km = TimeSeriesKMeans(n_clusters=n, random_state=1234, metric=metric,max_iter=1000)
labels = km.fit_predict(nm_data)

fig, axes = plt.subplots(n, figsize=(8.0, 18.0))
plt.subplots_adjust(hspace=0.5)
for i in range(n):
    ax = axes[i]
    for xx,label in zip(nm_data[labels == i],subject_acc_df.index[labels == i]):
        ax.plot(xx.ravel(), "k-", alpha=.2,label=label)
    ax.plot(km.cluster_centers_[i].ravel(), "r-")
    
    nm_ymin, nm_ymax = (-0.5,1)
    ax.set_ylim(nm_ymin, nm_ymax)
    datanum = np.count_nonzero(labels == i)
    ax.text(0.5, (nm_ymax*0.9+nm_ymin*0.1), f'Cluster {(i + 1)} : n = {datanum}')
    if i == 0:
        ax.set_title(metric.capitalize() + " k-means")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
# %%
