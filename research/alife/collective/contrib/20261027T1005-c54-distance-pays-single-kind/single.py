"""(c54) Single-kind populations (all mar 40 or all mar 60, mutation off) with and without birth-site depletion: what does the
stronger Marangoni coefficient cost? Per run, from c00's extract.py table and c50's spread_stats.py json: bodies over time
(mean over t >= 500), persistent splits and vanishings (fate counts over tracks), vanishings per split, track mean area,
path speed, and among dividing rods the M-gate passers, median D and median cycle. usage: single.py anadir seed [seed ...]"""
import sys, json, numpy as np
A = sys.argv[1]; seeds = [int(x) for x in sys.argv[2:]]
print("seed arm      bodies  splits vanish  van/split  area_mean  vpath_med  dividers pass  medD  cycle  ringpol")
for s in seeds:
    for a in ["m40dep", "m60dep", "m40E", "m60E"]:
        try:
            J = json.load(open(f"{A}/{a}_s{s}.json")); T = json.load(open(f"{A}/{a}_s{s}.table.json"))["rows"]
        except FileNotFoundError:
            continue
        tr = np.array([x[:7] for x in J["traj"]], float); t = tr[:, 0] * 5
        nb = tr[t >= 500, 1].mean()
        fates = [r["fate"] for r in T]
        nsp = sum(f == "divides" for f in fates); nva = sum(f in ("vanishes", "dies", "dissolves") for f in fates)
        long = [r for r in T if r["n"] >= 10]
        am = np.mean([r["A_mean"] for r in long]); vp = np.median([r["vpath"] for r in long])
        rp = np.nanmedian([r["ring_pol_rl"] for r in long if r.get("ring_pol_rl") is not None])
        D = J["div"]; pa = sum(d["pass_rl"] for d in D)
        print(f"{s} {a:7s} {nb:7.1f} {nsp:6d} {nva:6d}   {nva / max(nsp, 1):6.2f}   {am:8.1f}   {vp:8.3f}   {len(D):5d}   {pa:3d}  {np.median([d['D'] for d in D]) if D else np.nan:5.2f} {np.median([d['cycle'] for d in D]) if D else np.nan:6.0f}  {rp:.3f}")
    print(" fates seen:", sorted(set(fates)))
