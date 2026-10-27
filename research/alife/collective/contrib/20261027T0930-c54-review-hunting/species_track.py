"""(c54) Per-species bookkeeping for 20261026T2103-c46-hunting-ecology-claim: segment one render channel alone (prey c_a = channel 0,
predator c_b = channel 1; > thr, periodic, min area 6 px), run labkit's tracker and lineage (K = 5 frames, merge-aware), print the
body count every 10 frames and the persistent splits / generations; with a second channel, the share of splits whose parent
touched the other species within 3 px in the 3 frames before (splits during or right after a meal).
usage: species_track.py frames.npz channel [thr=0.5] [other_channel]"""
import sys, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
from scipy import ndimage as ndi
F = np.load(sys.argv[1]); ch = int(sys.argv[2]); thr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
oth = int(sys.argv[4]) if len(sys.argv) > 4 else None
R = F["render"].astype(np.float32); x = R[:, ch]; T, H, W = x.shape; rf = F["render_f"]
comps, links = LR._segment_frames(x, thr, 6, True)
tracks, ev = M.track(comps, links, (H, W), True); byid = {t["id"]: t for t in tracks}
lin = M.lineage_stats(tracks, ev, T, 100.0, (H, W), True, 5)
n = [c["n"] for c in comps]
print(f"channel {ch} > {thr}: bodies every 10 frames (t, n):", [(int(rf[i]) * 100, n[i]) for i in range(0, T, 10)])
print("lineage:", {k: (v if isinstance(v, (int, float)) else len(v)) for k, v in lin.items() if isinstance(v, (int, float, list))})
if oth is not None:
    near = 0; ps = lin["persistent_splits"]
    for e in ps:
        f0 = e["frame"]; tr = byid[e["parent"]]; ok = False
        for f in range(max(0, f0 - 3), f0):
            if f < tr["start"] or f > tr["end"]: continue
            lab = comps[f]["lab"]; c = tr["comp"][f - tr["start"]]
            m = ndi.binary_dilation(lab == c + 1, iterations=3) if (lab == c + 1).any() else None
            if m is not None and (R[f, oth][m] > 0.5).any(): ok = True
        near += ok
    print(f"persistent splits whose parent touched channel {oth} in the 3 frames before: {near}/{len(ps)}")
