"""a* calibrated on the in-world neutral twin (o_measure.report with the twin as reference); real vs twin late cohort novelty.
usage: twincal.py tag twin_tag seeds..."""
import sys, os, json, numpy as np
import analyze as A
om = A.om
tag, twin = sys.argv[1], sys.argv[2]; out = {}
for seed in map(int, sys.argv[3:]):
    log, rec, m = A.load(tag, seed); tl, _, _ = A.load(twin, seed); p = m["prm"]; T = int(m["t_end"]) // A.WIN * A.WIN; bw = 1.0
    for sp, n0, nm in ((0, p["Np0"], "prey"), (1, p["Nq0"], "pred")):
        S = A.species(log, sp, n0, bw, T); W = A.species(tl, sp, n0, bw, T)
        for q in (99.0, 99.9):
            r = om.report(S["t"], S["k"], W["t"], W["k"], T, Lc=A.LC, win=A.WIN, q=q)
            out[f"s{seed}_{nm}_q{q}"] = dict(astar=r["astar"], late_real=r["late_sig"], late_twin=r["late_ref_sig"], sig=r["sig"], twin_sig=r["ref_sig"])
            print(seed, nm, "q", q, "a*", round(r["astar"]), "late real", r["late_sig"], "late twin", r["late_ref_sig"], "| per window real", r["sig"][2:])
json.dump(out, open(f"data/{tag}_vs_{twin}_twincal_lc{A.LC}.json", "w"), indent=1)
