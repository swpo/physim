import sys, os, numpy as np, json, importlib.util
BLOBS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("csim", os.path.join(BLOBS, "composite", "sim.py"))
csim = importlib.util.module_from_spec(spec); spec.loader.exec_module(csim)
st = np.load(os.path.join(BLOBS, "composite", "data", "stamp_P7s_dx05.npz"))
stamp = dict(du=st["du"], dv=st["dv"], dw=st["dw"])
L=64.0; dx=0.5; c=L/2; d0=16.5
u0 = csim.uniform_state(2.0, -0.7, 1.0, 1.5)
u, v, w = csim.make_world_from_stamp(L, dx, u0, stamp, [(c, c-d0/2), (c, c+d0/2)])
p = dict(tau=2.5, Dv=2.0)
r = csim.run_fields(u, v, w, p, float(sys.argv[1]), dx, L, rec_tu=100.0)
seps=[]
for t, pos in zip(r["t"], r["pos"]):
    if len(pos)==2:
        d = csim.min_image(pos[1]-pos[0], L)
        seps.append([float(t), float(np.hypot(*d))])
print(json.dumps(dict(tag="composite_engine", status=r["status"], sep=seps,
                      ncomp_final=int(r["ncomp"][-1]))))
