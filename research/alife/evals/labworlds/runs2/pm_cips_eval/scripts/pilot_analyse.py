"""Pilot readouts: what each program changes at the probes (native, zero noise) and how each ablation's response
to its program differs from the native response. Units: native member spread at noise (per sensor and field:
RMS over nodes and the 13 score times of the across-member sd of a noisy native ensemble on the sham program).

  visibility(prog)           = RMS_{nodes,t}((nat_prog - nat_sham) / spread)
  ablation_total(abl, prog)  = RMS((abl_prog - nat_prog) / spread)
  response_diff(abl, prog)   = RMS(((abl_prog - abl_sham) - (nat_prog - nat_sham)) / spread)   (program-specific part)
"""
import sys, json, glob, os
import numpy as np
OUT = "/home/user/evalwork/pm_cips_eval"
world = sys.argv[1]
spread_file = sys.argv[2]          # npz with q0,q1,q2 member arrays (members, times, ports, slots) on sham, TIMES
TIMES = [0, 2, 5, 8, 10, 12, 15, 20, 22, 25, 30, 35, 40, 45, 50]
SCORE = [2, 5, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]
fields = ("S", "K", "L", "phi") if world == "pm" else ("e", "p", "F", "s")
z = np.load(spread_file)
qs = [z[k] for k in sorted(k for k in z.files if k.startswith("query"))] if "query0" in z.files else \
    [np.stack([z[f"m{m}_q{q}"] for m in range(2)]) for q in range(3)]
ti = [TIMES.index(t) for t in SCORE] if "query0" in z.files else [k for k in range(1, 11)]   # cips noise runs: every 5 tu
if "query0" not in z.files:
    qs = [q[:, 0] for q in qs]          # (members, times, ports, slots)
spread = {}
for qi, s in enumerate(("d0", "d1", "gl")):
    a = qs[qi][:, ti]
    sd = a.std(axis=0, ddof=1)                     # (times, ports, slots)
    for p, f in enumerate(fields):
        spread[(s, f)] = float(np.sqrt((sd[:, p, :] ** 2).mean())) + 1e-12
D = f"{OUT}/pilot/{world}"
runs = {os.path.basename(p)[:-4]: np.load(p) for p in sorted(glob.glob(f"{D}/*.npz"))}


def readout(r, s):
    times = list(r["times"])
    idx = [times.index(t) for t in SCORE]
    return r[s][idx]


def rms(diff, s, f, p):
    return float(np.sqrt(((diff[:, p, :] / spread[(s, f)]) ** 2).mean()))


res = {"spread": {f"{s}/{f}": v for (s, f), v in spread.items()}, "visibility": {}, "ablation": {}}
nat_sham = runs["native__sham"]
for k, r in runs.items():
    v, prog = k.split("__")
    if v != "native" or prog == "sham":
        continue
    res["visibility"][prog] = {s: {f: round(rms(readout(r, s) - readout(nat_sham, s), s, f, p), 2) for p, f in enumerate(fields)}
                               for s in ("d0", "d1", "gl")}
for k, r in runs.items():
    v, prog = k.split("__")
    if v == "native":
        continue
    nat = runs[f"native__{prog}"]
    ab_sham = runs.get(f"{v}__sham")
    e = {}
    for s in ("d0", "d1", "gl"):
        e[s] = {}
        for p, f in enumerate(fields):
            tot = rms(readout(r, s) - readout(nat, s), s, f, p)
            spec = None
            if ab_sham is not None and prog != "sham":
                spec = rms((readout(r, s) - readout(ab_sham, s)) - (readout(nat, s) - readout(nat_sham, s)), s, f, p)
            e[s][f] = [round(tot, 2), None if spec is None else round(spec, 2)]
    res["ablation"][k] = e
json.dump(res, open(f"{D}/analysis.json", "w"), indent=1)
print("spread", {k: round(v, 4) for k, v in res["spread"].items()})
print("\nvisibility vs sham (native): per sensor, per field")
for prog, v in res["visibility"].items():
    print(f"{prog:18s}", " | ".join(f"{s}: " + " ".join(f"{x:6.1f}" for x in v[s].values()) for s in v))
print("\nablation: [total vs native on the same program, program-specific response difference]")
for k, e in res["ablation"].items():
    print(f"{k:22s}", " | ".join(f"{s}: " + " ".join(f"{x[0]:.1f}/{x[1] if x[1] is not None else '-'}" for x in e[s].values()) for s in e))
