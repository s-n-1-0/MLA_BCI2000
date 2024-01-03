# %%
import numpy as np
for lap in [1,2]:
    data = np.load(f"./s{lap}_erders_ignores.npy")
    data.shape
    print(f"s{lap}")
    print(np.sum(data,axis=(0,1,2)))

# %%
