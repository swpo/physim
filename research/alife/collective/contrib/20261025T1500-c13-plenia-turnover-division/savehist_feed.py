import sys, os, importlib.util as u, numpy as np, pickle
os.environ["WORLD_P"] = sys.argv[1]; T = int(sys.argv[2]); every = int(sys.argv[3]); seed = int(sys.argv[4]); out = sys.argv[5]
s = u.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py")); w = u.module_from_spec(s); s.loader.exec_module(w)
st = w.init(seed, (128, 128)); H = []
for n in range(T + 1):
    if n % every == 0: H.append((st["id"].copy(), st["p"].astype(np.float32).copy()))
    if n < T: w.step(st)
pickle.dump(H, open(out, "wb"))
print("final N", len(st["p"]))
