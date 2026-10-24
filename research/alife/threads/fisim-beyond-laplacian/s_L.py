"""Heredity window: does an h-on cell keep its marker through T=400? Gated vs ungated (L)."""
import sys, json
from screen import *
from scipy import ndimage
import evo
rows = []
grid = [("L", Dh, kb) for Dh in (0.02, 0.05, 0.1) for kb in (0.225, 0.25, 0.275)] + [("N", 0.3, kb) for kb in (0.225, 0.25, 0.275)]
for arm, Dh, kb in grid:
    g = evo.genome(arm, kb=kb, DhL=Dh)
    F = soup(g, 128, 0, n=10, acts=[0], dress_chans=[0, 1])
    u0 = g["acts"][0]["u0"]; u0h = g["acts"][1]["u0"]
    lab, k = ndimage.label(F[0] - u0 > 0.5); cs = ndimage.center_of_mass(F[0] - u0, lab, range(1, k + 1))
    for j in np.random.default_rng(100).permutation(k)[:k // 2]:
        X.poke(F, 1, cs[j][0] * 0.5, cs[j][1] * 0.5, 2.2, 2.5, 0.5)
    sn, ts, w = run(g, N=128, T=400, F=F, nsnap=5)
    out = []
    for s in sn:
        lab, n = ndimage.label(s[0] - u0 > 0.45 * (np.sqrt(2) - u0))
        hm = ndimage.mean(s[1] - u0h, lab, range(1, n + 1)) if n else []
        out.append((n, int(np.sum(np.array(hm) > 1.0))))
    line = f"Lgrid arm={arm} Dh={Dh} kb={kb}: (cells, on) {out}"
    print(line, flush=True); open("screens/log.txt", "a").write(line + "\n")
    if arm == "L" and Dh == 0.05 or arm == "N":
        strip(sn[:, [0, 1, 4]], ts, ["u", "h", "m"], f"screens/Lgrid_{arm}_Dh{Dh}_kb{kb}.png", line)
