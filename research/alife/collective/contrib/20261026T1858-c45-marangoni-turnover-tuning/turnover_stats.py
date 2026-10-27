"""(c45) Demography and cohort penetrance of the Marangoni rods under trait-blind dilution.
usage: turnover_stats.py table.json metrics.json dilution.log.jsonl [window_frames=20] [cohort_frames=24]
table.json from c00's extract.py (K=20). Per window: bodies (mean components), persistent splits (labkit, K=20), removals
(dilution log), other deaths (tracks that vanish at a frame that is not just before a dilution event), merges (tracks born
by merge), max generation reached (persistent-split tree from labkit metrics). Per birth cohort of dividing tracks
(split-born, >= 2 daughters living >= 20 frames): n, median D (rod lengths), share D >= 3 (rod lengths) and D_A >= 3
(sqrt(area))."""
import sys, json, numpy as np
tab = json.load(open(sys.argv[1])); met = json.load(open(sys.argv[2]))
log = [json.loads(l) for l in open(sys.argv[3])] if len(sys.argv) > 3 and sys.argv[3] != "-" else []
WIN = int(sys.argv[4]) if len(sys.argv) > 4 else 20; COH = int(sys.argv[5]) if len(sys.argv) > 5 else 24
rows = tab["rows"]; T = tab["T"]
gen = {}
for ev in sorted(met.get("persistent_splits", []), key=lambda e: e["frame"]):
    g = gen.get(ev["parent"], 0) + 1
    for c in ev["children"]: gen[c] = g
splits_f = [e["frame"] for e in met.get("persistent_splits", [])]
dil_frames = set(int(e["frame"]) for e in log)
rem = {}
for e in log: rem[int(e["frame"])] = rem.get(int(e["frame"]), 0) + len(e["removed"])
ncomp = [len(x) for x in met.get("series", {}).get("areas", [])] if isinstance(met.get("series"), dict) and "areas" in met["series"] else None
print(f"frames {T}; dilution events {len(log)}, removed {sum(rem.values())} bodies; persistent splits {len(splits_f)}; max generation {max(gen.values(), default=0)}")
print("window      splits removed other_deaths merges_born  maxgen_born  bodies_at_dilution")
for w0 in range(0, T, WIN):
    w1 = w0 + WIN
    sp = sum(w0 <= f < w1 for f in splits_f)
    rm = sum(v for f, v in rem.items() if w0 <= f < w1)
    od = sum(1 for r in rows if r["fate"] == "vanishes" and w0 <= r["end"] < w1 and (r["end"] + 1) not in dil_frames)
    mg = sum(1 for r in rows if r["birth"] == "merge" and w0 <= r["start"] < w1)
    mgen = max([gen.get(r["id"], 0) for r in rows if w0 <= r["start"] < w1] or [0])
    nb = [e["n"] for e in log if w0 <= e["frame"] < w1]
    print(f"{w0:4d}-{w1:4d} {sp:7d} {rm:7d} {od:12d} {mg:11d} {mgen:12d}   {nb}")
print("birth cohort  n_div  median_D  share_D>=3  share_DA>=3")
dv = [r for r in rows if r["dividing"]]
for c0 in range(0, T, COH):
    g = [r for r in dv if c0 <= r["start"] < c0 + COH]
    if not g: continue
    D = np.array([r["disp_rl"] for r in g]); DA = np.array([r["net"] / np.sqrt(r["A_mean"]) for r in g])
    print(f"{c0:4d}-{c0+COH:4d} {len(g):6d} {np.median(D):9.2f} {np.mean(D >= 3):10.2f} {np.mean(DA >= 3):11.2f}")
D = np.array([r["disp_rl"] for r in dv])
print(f"all dividing: n {len(dv)}, median D {np.median(D) if len(D) else float('nan'):.2f}, D>=3: {int((D >= 3).sum())} of {len(dv)}")
