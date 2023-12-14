# %%
import json
import matplotlib.pyplot as plt
import numpy as np
from tslearn.clustering import TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from load_excel import get_data_from_excel
with open('settings.json') as f:
    settings = json.load(f)
    lap_id = settings["lap_id"]
    dataset_dir = settings["dataset_dir"] + "/" + lap_id
subject_acc_df = get_data_from_excel(f"{dataset_dir}/evals/acc_d2_results.xlsx").iloc[:,1:]
print(subject_acc_df)
# %%
n = 3
nm_data = subject_acc_df.values#TimeSeriesScalerMeanVariance().fit_transform(subject_acc_df.values)
nm_data = nm_data - nm_data.mean(axis=1,keepdims=True)
print(nm_data.mean(axis=1).shape)
distortions = [] 
for i in range(1,17): 
    ts_km = TimeSeriesKMeans(n_clusters=i, random_state=1234, metric="euclidean",max_iter=1000)
    ts_km.fit_predict(nm_data)
    distortions.append(ts_km.inertia_) 

plt.plot(range(1,17),distortions,marker="o") 
plt.xticks(range(1,17)) 
plt.xlabel("Number of clusters") 
plt.ylabel("Distortion") 
plt.show()

km_euclidean = TimeSeriesKMeans(n_clusters=n, random_state=1234, metric="euclidean",max_iter=1000)
labels_euclidean = km_euclidean.fit_predict(nm_data)

fig, axes = plt.subplots(n, figsize=(8.0, 18.0))
plt.subplots_adjust(hspace=0.5)
for i in range(n):
    ax = axes[i]
    for xx in nm_data[labels_euclidean == i]:
        ax.plot(xx.ravel(), "k-", alpha=.2)
    ax.plot(km_euclidean.cluster_centers_[i].ravel(), "r-")
    
    nm_ymin, nm_ymax = (-0.2,0.2)
    ax.set_ylim(nm_ymin, nm_ymax)
    datanum = np.count_nonzero(labels_euclidean == i)
    ax.text(0.5, (nm_ymax*0.9+nm_ymin*0.1), f'Cluster {(i + 1)} : n = {datanum}')
    if i == 0:
        ax.set_title("Euclidean k-means")
# %%
