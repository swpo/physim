import sys, importlib.util, numpy as np, pickle
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = pickle.load(open(sys.argv[2], "rb")); dt = w.P["dt"]
def labs():
    u = s["u"] - w.P["u_bg"]; body = u > 0.8
    lab, n = ndimage.label(body); far = ~ndimage.binary_dilation(body, iterations=3)
    return lab, n, far
lab0, n, far = labs()
sz = ndimage.sum(lab0 > 0, lab0, range(1, n + 1))
big = [k + 1 for k in np.argsort(-sz)[:6]]
emptied, ctrl = big[:3], big[3:]
cy = {k: ndimage.center_of_mass(lab0 == k) for k in big}
for k in emptied: s["c"][ndimage.binary_dilation(lab0 == k, iterations=3)] = 0
def con():
    lab, n, far = labs(); co = s["c"][far].mean(); out = {}
    for k, (y, x) in cy.items():
        j = lab[int(round(y)) % lab.shape[0], int(round(x)) % lab.shape[1]]
        out[k] = s["c"][lab == j].mean() / co if j else float("nan")
    return out
tt = 0.0
for t in [0, 1, 2, 5, 10, 20, 40, 80, 160]:
    while tt < t - 1e-9: s = w.step(s); tt += dt
    c = con()
    print(f"t0+{t}: emptied " + " ".join(f"{c[k]:.1f}x" for k in emptied) + " | controls " + " ".join(f"{c[k]:.1f}x" for k in ctrl), flush=True)
