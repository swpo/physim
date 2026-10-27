"""(c54) Consumer-only bookkeeping for 20261026T1700-c43-cips-consumer: segment the consumer channel q alone (render channel 1,
q > thr, periodic, min area 6 px) and run labkit's own tracker, so splits and generations are of consumer bodies, not of the
prey+consumer composite that the pack's matter [0, 1] tracks. Also: share of consumer bodies touching a prey droplet (prey
channel c_a > 0.5 within 2 px), consumer body count over time, and persistent consumer splits whose two daughters each sit on
a different prey droplet (joint division) vs on the same droplet. usage: consumer_only.py frames.npz [thr=0.5] [K=5]"""
import sys, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
from scipy import ndimage as ndi
F = np.load(sys.argv[1]); thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5; K = int(sys.argv[3]) if len(sys.argv) > 3 else 5
R = F["render"].astype(np.float32); q = R[:, 1]; a = R[:, 0]; T, H, W = q.shape
comps, links = LR._segment_frames(q, thr, 6, True)
tracks, ev = M.track(comps, links, (H, W), True)
lin = M.lineage_stats(tracks, ev, T, 100.0, (H, W), True, K)
n = [c["n"] for c in comps]
print(f"consumer bodies (q>{thr}): t0 {n[0]}, t1000 {n[10]}, t6000 {n[60]}, end {n[-1]}; mean over t>=2000 {np.mean(n[20:]):.1f}")
# touching prey
tot = touch = 0
for f in range(20, T, 10):
    lab, m = ndi.label(q[f] > thr)
    prey = ndi.binary_dilation(a[f] > 0.5, iterations=2)
    for i in range(1, m + 1):
        b = lab == i
        if b.sum() < 6: continue
        tot += 1; touch += bool((b & prey).any())
print(f"consumer bodies touching prey (sampled every 10 frames from t 2000): {touch}/{tot}")
print("consumer-only lineage:", {k: (v if isinstance(v, (int, float)) else len(v)) for k, v in lin.items() if isinstance(v, (int, float, list))})
ps = lin.get("persistent_splits", [])
print("persistent consumer splits:", len(ps) if isinstance(ps, list) else ps, "| example:", ps[:2] if isinstance(ps, list) else "")
