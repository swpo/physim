"""c13: fate of the locally starved cell vs the rest. From labkit frames.npz (matter channel, one frame per 500 t):
at frame 120 (t=60000) take the fed run's cells (matter > half its max), pick the one nearest the centre (as world_local
does with phi>0.5), dilate 8 px = the cut disk. Report matter inside the disk and outside it over time in fed, local-cut
and global-cut runs, and the number of cells (components >= 20 px) outside the disk."""
import numpy as np
from scipy import ndimage
runs = {k: np.load(f"rerun_{k}/seed6/frames.npz")["matter"] for k in ("world", "world_local", "world_starve")}
m0 = runs["world"][120]; thr = 0.5 * m0.max(); lab, n = ndimage.label(m0 > thr)
H, W = m0.shape; best, bd = 0, 1e9
for k in range(1, n + 1):
    ys, xs = np.nonzero(lab == k)
    if len(ys) < 20: continue
    d = (ys.mean() - H / 2) ** 2 + (xs.mean() - W / 2) ** 2
    if d < bd: best, bd = k, d
cut = ndimage.binary_dilation(lab == best, iterations=8)
print("cut cell px", int((lab == best).sum()), "disk px", int(cut.sum()))
print("frame t | inside disk: fed local global | outside: fed local global | cells outside: fed local global")
for f in (118, 120, 121, 122, 124, 126, 130, 140, 160, 200):
    ins = [round(float(r[f][cut].sum()), 1) for r in runs.values()]; out = [round(float(r[f][~cut].sum()), 1) for r in runs.values()]
    nc = []
    for r in runs.values():
        l, k = ndimage.label((r[f] > thr) & ~cut); nc.append(int(sum(1 for i in range(1, k + 1) if (l == i).sum() >= 20)))
    print(f, f * 500, "|", ins, "|", out, "|", nc)
