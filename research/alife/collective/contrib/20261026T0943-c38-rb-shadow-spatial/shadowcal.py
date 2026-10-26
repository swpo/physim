"""Is the RB shadow a fair null for this spatial world? Score the in-world neutral twin itself against 8 RB shadows built
from its own ledger (a* = max over 3 shadows of the 99.9th pct, as in analyze.py). usage: shadowcal.py twin_tag seeds..."""
import sys, os, json, numpy as np
import analyze as A
om = A.om; out = {}
for seed in map(int, sys.argv[2:]):
    log, rec, m = A.load(sys.argv[1], seed); p = m["prm"]; T = int(m["t_end"]) // A.WIN * A.WIN
    for sp, n0, nm in ((1, p["Nq0"], "pred"), (0, p["Np0"], "prey")):
        S = A.species(log, sp, n0, 1.0, T)
        sh = [om.rb_shadow(S["t"], S["innov"], S["dt"], n0=[S["k0"]] * S["n0"], seed=q) for q in range(8)]
        ast = max(om.calibrate_astar(a, b, A.LC, 99.9, t0=A.WIN) for a, b in sh[:3])
        own = sum(om.cohort(S["t"], S["k"], T, ast, A.LC, A.WIN)["sig"][2:])
        env = sorted(sum(om.cohort(a, b, T, ast, A.LC, A.WIN)["sig"][2:]) for a, b in sh)
        out[f"s{seed}_{nm}"] = dict(astar=ast, twin_late=own, shadow_late=env)
        print(sys.argv[1], seed, nm, "a*", round(ast), "twin itself late", own, "its RB shadows", env, flush=True)
json.dump(out, open(f"data/shadowcal_{sys.argv[1]}.json", "w"), indent=1)
