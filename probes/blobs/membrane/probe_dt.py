import sys, numpy as np, json
sys.path.insert(0, ".")
import sim
tag, dt, T = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
L=64.0; c=L/2; d0=16.5
r = sim.run(tau1=2.5, Dv1=2.0, stamp1_name="stamp_P7s_dx05.npz", L=L, T=T, dt=dt,
            blobs1=[(c-d0/2, c, None), (c+d0/2, c, None)], rec_tu=100.0, save_fields=False)
sep = [float(np.hypot(*(p[1]-p[0]))) if len(p) == 2 else None for p in r["pos1"]]
out = dict(tag=tag, dt=dt, T=T, status=r["status"], ncomp_final=int(r["ncomp1"][-1]),
           ncomp=[int(x) for x in r["ncomp1"]],
           sep=[[float(t), s] for t, s in zip(r["t"], sep)])
print(json.dumps(out))
