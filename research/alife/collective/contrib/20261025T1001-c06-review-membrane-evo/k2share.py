"""K2 biomass share sum(K2)/sum(K1+K2) over recorded frames of a labkit frames.npz (channels K1, K2 first)."""
import sys, numpy as np
F = np.load(sys.argv[1]); X = F[[k for k in F.files if F[k].ndim == 4][0]]
for i in list(range(0, X.shape[0], 20)) + [X.shape[0] - 1]:
    k1, k2 = X[i, 0].sum(), X[i, 1].sum()
    print(i, round(float(k2 / max(k1 + k2, 1e-9)), 3), 'K total', round(float(k1 + k2), 1))
