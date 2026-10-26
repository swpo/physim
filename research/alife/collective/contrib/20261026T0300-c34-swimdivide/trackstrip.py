"""(c34) Biography of one labkit track, its parent and its children: 10 crops (s channel, phi=0 contour, fixed
colour scale) at evenly spaced frames of the track's life plus its two children 10 frames after the split, and
the track's centroid path drawn on the full domain. Same tracker as swimdivide.py.
usage: trackstrip.py frames.npz world.py track_id out.png [title]"""
import sys, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, __file__.rsplit("/collective/", 1)[0])
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32); R = F["render"].astype(np.float32); rf = list(F["render_f"])
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
tid = int(sys.argv[3]); meta = W.META
mn, thr, lo, hi = LR._normalize_matter(mat, meta, True, meta.get("threshold"))
H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, events = M.track(comps, links, (H, Wd), True)
T = {t["id"]: t for t in tracks}; t = T[tid]
ridx = {f: i for i, f in enumerate(rf)}  # matter frame f (0 = initial) -> render index
smax = np.percentile(R[-1, 2], 99.5); h = 14
fr = np.linspace(t["start"], t["end"], 10).round().astype(int)
kids = [T[c] for c in t["children"] if T[c]["birth"] == "split"][:2]
panels = [(t, f) for f in fr] + [(k, min(k["start"] + 10, k["end"])) for k in kids]
fig, ax = plt.subplots(1, len(panels) + 1, figsize=(2 * (len(panels) + 1) + 2, 2.6))
for a, (tr, f) in zip(ax, panels):
    i = f - tr["start"]; cy, cx = int(round(tr["cy"][i])), int(round(tr["cx"][i]))
    ys = np.arange(cy - h, cy + h) % H; xs = np.arange(cx - h, cx + h) % Wd
    k = ridx.get(f, min(range(len(rf)), key=lambda j: abs(rf[j] - f)))
    a.imshow(R[k, 2][np.ix_(ys, xs)], cmap="magma", vmin=0, vmax=smax, origin="lower")
    a.contour(R[k, 0][np.ix_(ys, xs)], [0], colors="c", linewidths=0.8)
    a.set_title(f"#{tr['id']} f{f}", fontsize=8); a.axis("off")
dy = np.concatenate([[0], np.cumsum(M._wrap(np.diff(t["cy"]), H))]); dx = np.concatenate([[0], np.cumsum(M._wrap(np.diff(t["cx"]), Wd))])
ax[-1].plot(t["cx"][0] + dx, t["cy"][0] + dy, "k-"); ax[-1].plot(t["cx"][0], t["cy"][0], "go"); ax[-1].plot(t["cx"][0] + dx[-1], t["cy"][0] + dy[-1], "rs")
ax[-1].set_aspect("equal"); ax[-1].set_title(f"path, net {np.hypot(dy[-1], dx[-1]):.1f} px", fontsize=8)
fig.suptitle(sys.argv[5] if len(sys.argv) > 5 else f"track {tid}", fontsize=9); fig.tight_layout(); fig.savefig(sys.argv[4], dpi=80)
