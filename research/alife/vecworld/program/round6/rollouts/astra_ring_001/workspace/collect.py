import numpy as np
from physim2 import Lab
lab=Lab()
print(lab.card(),flush=True)
obs=[]
for j in range(10):
    obs.append(lab.experiment('stationary-long-'+str(j),19))
    np.savez('data_initial.npz',obs=np.array(obs))
    print(j,np.shape(obs[-1]),flush=True)
print(lab.usage())
