"""Screen a thread world with parameter overrides: python wscreen.py WORLD tag steps key=val ..."""
import ast, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.world import load_world
import screen as S

def main():
    wp, tag, nsteps = sys.argv[1], sys.argv[2], int(sys.argv[3])
    over = {}
    seed = 0
    for a in sys.argv[4:]:
        k, v = a.split("=", 1)
        if k == "seed":
            seed = int(v); continue
        over[k] = ast.literal_eval(v)
    W = load_world(wp)
    s = W.init(seed, W.META["size"], **over)
    L = s["p"]["L"]
    snaps, counts = [], []
    every = nsteps // 11
    t0 = time.time()
    for n in range(nsteps + 1):
        if n % every == 0:
            snaps.append((n * W.META["dt"], s["x"].copy(), s["t"].copy()))
        if n % 50 == 0:
            counts.append(np.bincount(s["t"], minlength=4))
        if n < nsteps:
            s = W.step(s)
    cnt = np.array(counts)
    title = f"{W.META['name']} {tag}: " + " ".join(sys.argv[4:])
    S.sheet(snaps, L, f"screens/{tag}.png", title[:150])
    np.savez_compressed(f"scratch/{tag}.npz", x=np.stack([q[1] for q in snaps]), t=np.stack([q[2] for q in snaps]), counts=cnt)
    print(f"{tag}: {time.time()-t0:.0f}s counts start {cnt[0]} mid {cnt[len(cnt)//2]} end {cnt[-1]}")

main()
