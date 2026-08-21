"""rotorhunt.py — targeted loop test: does merge+select REDISCOVER the rotor?

Pool: M4 family refs ONLY (tau in {4.5, 5.0, 5.7, 5.9} — note NONE of these
is the certified rotor pair (5.7, 2.5); tau2 must come from MUTATION).
Operator: merge_cross_edge (eta ~ logU[0.03, 0.3], symmetric p=0.8) with
post-merge mutation p=0.5. Assay: funnel + A1 panel on both acts + A4 only
(pair/dial skipped: the question is the cross-species phenotype).
Stop when a child classifies rotor or n exhausted. Lineage logged.
"""
import sys, os, json, time
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
L0DIR = os.path.dirname(BASE)
sys.path.insert(0, os.path.join(L0DIR, "lib"))
sys.path.insert(0, BASE)

import genome as G
import funnel as FU
import assays as AS
import operators_lib as OP
from assays_x import a4_cross
from evolve import append_result, archive_update, ARCHIVE, ARCHIVE_X

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 7000
    tag = "rh1"
    refs = [G.ref_M4(4.5), G.ref_M4(5.0), G.ref_M4(5.7), G.ref_M4(5.9)]
    for j in range(n):
        rng = np.random.default_rng(seed0 + j)
        p1 = refs[rng.integers(len(refs))]
        p2 = refs[rng.integers(len(refs))]
        eta = float(np.exp(rng.uniform(np.log(0.03), np.log(0.3))))
        sym = bool(rng.random() < 0.8)
        child, info = OP.merge_cross_edge(p1, p2, eta=eta, symmetric=sym)
        lin = dict(op="merge_cross_edge", parents=[p1["id"], p2["id"]],
                   params=dict(eta=eta, symmetric=sym))
        if child is not None and rng.random() < 0.5:
            m, mi = OP.mutate(child, rng, p_struct=0.0)
            if m is not None:
                child = m
                lin["post_mutate"] = mi.get("moves")
        cand = f"{tag}_{seed0+j}"
        rec = dict(kind="evo_child", cand=cand, tag=tag, gen=0, lineage=lin)
        t00 = time.time()
        if child is None:
            rec["stage"] = "op_fail"
            append_result(rec)
            continue
        child["id"] = cand
        rec["genome"] = G.genome_json(child)
        fr = FU.funnel(child)
        rec.update({k: fr[k] for k in fr if k != "stage"})
        rec["stage"] = fr["stage"]
        if fr["stage"] != "pass":
            rec["total_s"] = round(time.time() - t00, 2)
            append_result(rec)
            print(cand, "funnel", fr["stage"], flush=True)
            continue
        a1 = {}
        nrun = 0
        for i in range(len(child["acts"])):
            a1[i] = AS.a1_panel(child, i)
            nrun += 1 if a1[i].get("variant") == "bare" else 2
        rec["a1"] = a1
        alive = [i for i in a1 if a1[i]["cls"] in ("persist", "travel")]
        if len(alive) >= 2:
            d0f = 0.6 if a1[alive[0]].get("variant") == "dressed0.6" else 0.0
            d1f = 0.6 if a1[alive[1]].get("variant") == "dressed0.6" else 0.0
            rec["a4"] = a4_cross(child, alive[0], alive[1], dress0=d0f, dress1=d1f)
            nrun += 1
            rec["cross_sig"] = rec["a4"]["cls"]
        else:
            rec["cross_sig"] = "na"
        rec["n_assays"] = nrun
        rec["stage"] = "assayed"
        rec["total_s"] = round(time.time() - t00, 2)
        # extended-archive insert only (no full descriptor computed)
        keyx = f"rotorhunt|{rec['cross_sig']}"
        archive_update(ARCHIVE_X, keyx, fr["g0a_margin"], child, cand,
                       extra=dict(cross_sig=rec["cross_sig"], lineage=lin))
        append_result(rec)
        print(cand, f"eta={eta:.3f}", [round(c['tau'],2) for c in child['chans']],
              rec["cross_sig"],
              (f"omega={rec['a4']['omega']:.5f} sep={rec['a4']['sep_mean']:.2f}"
               if rec.get("a4") and "omega" in rec["a4"] else ""),
              f"{rec['total_s']:.0f}s", flush=True)
        if rec["cross_sig"] == "rotor":
            print("ROTOR REDISCOVERED at child", j + 1, flush=True)

if __name__ == "__main__":
    main()
