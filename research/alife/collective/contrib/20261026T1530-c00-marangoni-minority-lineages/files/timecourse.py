"""Time course of a Marangoni run in 20-frame windows: bodies, mean area, mean centroid speed, splits/merges,
bath and ring surfactant, bath cargo, order inside bodies. usage: timecourse.py frames.npz world.py label dx"""
import sys, importlib.util, numpy as np
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4])); sys.dont_write_bytecode = True
from labkit import run as LR, metrics as M
from scipy import ndimage as ndi
fn, wpath, label, dx = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
F = np.load(fn); mat = F["matter"].astype(np.float32); render = F["render"]; rf = list(F["render_f"])
spec = importlib.util.spec_from_file_location("w", wpath); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); T = len(comps)
step = np.full(T, np.nan); stepsum = np.zeros(T); stepn = np.zeros(T)
for t in tracks:
    if len(t["cy"]) < 2: continue
    st = np.hypot(M._wrap(np.diff(t["cy"]), H), M._wrap(np.diff(t["cx"]), Wd)) * dx
    for k, s in enumerate(st): stepsum[t["start"] + k + 1] += s; stepn[t["start"] + k + 1] += 1
win = 20
print(f"{label}: window  bodies  meanA  speed(u/t)  splits merges  bath_s  ring_s  core_s  bath_c  |Q|in")
for w0 in range(0, T - 1, win):
    fr = range(max(w0, 1), min(w0 + win, T))
    nb = np.mean([len(comps[f]["area"]) for f in fr]); ma = np.mean([np.mean(comps[f]["area"]) if len(comps[f]["area"]) else 0 for f in fr]) * dx * dx
    sp = stepsum[list(fr)].sum() / max(stepn[list(fr)].sum(), 1) / 5.0
    ns = sum(1 for e in ev if e["type"] == "split" and w0 <= e["frame"] < w0 + win); nm = sum(1 for e in ev if e["type"] == "merge" and w0 <= e["frame"] < w0 + win)
    bs, rs, cs, bc, qi = [], [], [], [], []
    for f in fr:
        if f not in rf: continue
        i = rf.index(f); body = comps[f]["lab"] > 0
        bw = np.pad(body, 6, mode="wrap")
        far = ~ndi.binary_dilation(bw, iterations=6)[6:-6, 6:-6]
        band = ndi.binary_dilation(bw, iterations=2)[6:-6, 6:-6] & ~ndi.binary_erosion(bw, iterations=1)[6:-6, 6:-6]
        core = ndi.binary_erosion(bw, iterations=2)[6:-6, 6:-6]
        s = render[i, 2].astype(float); c = render[i, 3].astype(float); q = render[i, 1].astype(float)
        bs.append(s[far].mean()); rs.append(s[band].mean() if band.any() else np.nan); cs.append(s[core].mean() if core.any() else np.nan)
        bc.append(c[far].mean()); qi.append(q[body].mean() if body.any() else np.nan)
    print(f"  {w0:3d}-{min(w0 + win, T) - 1:3d}  {nb:6.1f} {ma:6.1f}  {sp:9.3f}  {ns:5d} {nm:6d}  {np.nanmean(bs):.4f}  {np.nanmean(rs):.3f}  {np.nanmean(cs):.3f}  {np.nanmean(bc):.3f}  {np.nanmean(qi):.3f}")
