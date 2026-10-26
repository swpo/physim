import importlib.util, sys, numpy as np
def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
A = load(sys.argv[1], "a"); B = load(sys.argv[2], "b")
sa, sb = A.init(51, (128, 128)), B.init(51, (128, 128))
for i in range(int(sys.argv[3])):
    sa = A.step(sa); sb = B.step(sb)
for k in ("phi", "q1", "q2", "s", "vx", "c"):
    print(k, "max|diff|", float(np.abs(sa[k] - sb[k]).max()), "identical", bool(np.array_equal(sa[k], sb[k])))
print("s2 range", float(sb["s2"].min()), float(sb["s2"].max()), "s range", float(sb["s"].max()))
