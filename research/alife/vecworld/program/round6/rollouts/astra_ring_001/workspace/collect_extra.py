import numpy as np
from physim2 import Lab
lab=Lab()
obs=[]
for j in range(200):
    obs.append([lab.reset('independent-stationary-'+str(j))])
    np.savez('data_extra.npz',obs=np.array(obs))
    if j%25==24: print(j+1,flush=True)
print(lab.usage())
