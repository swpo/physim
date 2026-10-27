"""(c54) Cross-kind merges in the competition assay: for every labkit merge event (child with >= 2 parent tracks), the kind of each
parent at its last rendered frame and the kind of the merged child at its first rendered frame (argmax of the summed s_k over the
body, render channels 2-4). Counts merges of a mar-40 (k1) and a mar-60 (k2) body by the child's kind; also the kinds of bodies
that vanish (end without children before the run end). usage: merges.py frames.npz world.py"""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32); R = F["render"]; rf = [int(x) for x in F["render_f"]]; ri = {f: i for i, f in enumerate(rf)}
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
def kind(tr, which):
    fr = range(tr["start"], tr["end"] + 1); fr = list(fr) if which == "first" else list(fr)[::-1]
    for f in fr:
        if f in ri:
            m = comps[f]["lab"] == tr["comp"][f - tr["start"]] + 1
            if m.any(): return int(np.argmax([R[ri[f], 2 + k][m].astype(float).sum() for k in range(3)]))
    return None
out = {}
for t in tracks:
    if len(t["parents"]) >= 2:
        pk = tuple(sorted(kind(byid[p], "last") for p in t["parents"] if p in byid and kind(byid[p], "last") is not None))
        ck = kind(t, "first")
        if 1 in pk and 2 in pk: out[ck] = out.get(ck, 0) + 1
print("merges of a k1 and a k2 body, by child kind:", out)
