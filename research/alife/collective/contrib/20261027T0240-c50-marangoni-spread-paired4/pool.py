"""(c50) Paired-seed summary for Q:marangoni-swimmer-spread (plain design: E vs identical-event twin; seed 500 also C and drive-off).
Per run: trait mean (ladder value of living bodies, purity >= 0.6) at the last rendered frame and averaged over t >= 1000;
mar-60 share averaged over t >= 1000; M-gate passers among dividing rods (3 own rod lengths, rear tip >= 2/3), in all and in
dividing rods born after t 1000 (late); and the pooled E-minus-twin differences with a sign count over seeds.
usage: pool.py outdir seed [seed ...]"""
import sys, json, numpy as np
o = sys.argv[1]; seeds = [int(x) for x in sys.argv[2:]]
rows = []
print("seed arm   trait_end  trait_late  k2share_late  pass_all  pass_late  bodies_end")
for s in seeds:
    r = {}
    for a in ["E", "twin"]:
        J = json.load(open(f"{o}/{a}_s{s}.json")); tr = np.array([x[:7] for x in J["traj"]], float)
        t = tr[:, 0] * 5; n = tr[:, 2:5].sum(1); ok = n >= 3
        late = ok & (t >= 1000)
        tm_end = tr[ok, 5][-1]; tm_late = np.nanmean(tr[late, 5]); k2 = np.mean(tr[late, 4] / n[late])
        D = J["div"]; pa = sum(d["pass_rl"] for d in D); dl = [d for d in D if d["start"] * 5 >= 1000]; pl = sum(d["pass_rl"] for d in dl)
        r[a] = (tm_end, tm_late, k2, pa, len(D), pl, len(dl))
        print(f"{s} {a:5s} {tm_end:9.1f} {tm_late:10.1f} {k2:12.2f}   {pa}/{len(D)}     {pl}/{len(dl)}     {int(tr[-1, 1])}")
    rows.append((s, r["E"][1] - r["twin"][1], r["E"][0] - r["twin"][0], r["E"][3] / max(r["E"][4], 1) - r["twin"][3] / max(r["twin"][4], 1)))
R = np.array([x[1:] for x in rows])
print("E minus twin per seed (trait_late, trait_end, pass share):")
for x in rows: print(f"  {x[0]}: {x[1]:+.1f} {x[2]:+.1f} {x[3]:+.2f}")
print(f"seeds with E > twin: trait_late {int((R[:, 0] > 0).sum())}/{len(R)}, trait_end {int((R[:, 1] > 0).sum())}/{len(R)}, pass share {int((R[:, 2] > 0).sum())}/{len(R)}")
print(f"mean difference: trait_late {R[:, 0].mean():+.1f}, trait_end {R[:, 1].mean():+.1f}, pass share {R[:, 2].mean():+.3f}")
