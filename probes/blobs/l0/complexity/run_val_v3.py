"""run_val_v3.py — v3 METRICS VALIDATION GATE runner (V3_TRACKB_SPEC).
Banks: (a) registry worlds m0,m4,pred,coex,mv3 + champions p6g8_033,
p3g9_022,p4g2_044; (b) hand-built positives (worlds_v3.BANK_B); (c)
anti-gaming probes (worlds_v3.BANK_C).
Usage: python3 run_val_v3.py <name> [--seed N] [--workers N]
Writes logs_v3/<name>_s<seed>.json (full assay_v3 out, lean).
"""
import argparse, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import worlds as W1
import worlds_v3 as WV3
import assay_v3 as AV3
from assay_v3 import run_assay
import assay_v2 as AV2

FC = os.path.join(os.path.dirname(HERE), "deepsearch", "v2_analysis",
                  "film_candidates")
CHAMPS = ["p6g8_033", "p3g9_022", "p4g2_044"]
BANK_A = ["m0", "m4", "pred", "coex", "mv3"]
# T policy: 2500 flat; 5000 cap where the world needs the horizon
CAPS = dict(mv3=5000.0, m5_trains=5000.0,
            p6g8_033=5000.0, p3g9_022=5000.0, p4g2_044=5000.0)


def get_spec(name):
    if name in BANK_A:
        g = W1.WORLDS[name]()
        return dict(genome=g, ic=None,
                    kw=dict(kicks=W1.KICKS.get(g["id"])), bank="a",
                    note=f"GT world {g['id']}")
    if name in CHAMPS:
        g = json.load(open(os.path.join(FC, name + ".json")))["genome"]
        return dict(genome=g, ic=None, kw={}, bank="a",
                    note=f"v2 champion {name}")
    if name in WV3.BANK_B:
        d = WV3.BANK_B[name]()
        d["bank"] = "b"
        return d
    if name in WV3.BANK_C:
        d = WV3.BANK_C[name]()
        d["bank"] = "c"
        return d
    raise KeyError(name)


ALL = BANK_A + CHAMPS + list(WV3.BANK_B) + list(WV3.BANK_C)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    spec = get_spec(a.name)
    kw = dict(spec.get("kw") or {})
    cap = float(kw.pop("cap", CAPS.get(a.name, 2500.0)))
    outdir = os.path.join(HERE, "logs_v3")
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    out = run_assay(spec["genome"], seed=a.seed, workers=a.workers,
                    cap=max(cap, CAPS.get(a.name, 2500.0)),
                    tag=a.name, ic_override=spec.get("ic"),
                    verbose=True, **kw)
    d9 = out["D"].get("d9", {})
    row = dict(name=a.name, bank=spec.get("bank"), seed=a.seed,
               note=spec.get("note"),
               interest_v2=round(out.get("interest_v2", 0.0), 2),
               interest_v3=round(out.get("interest", 0.0), 2),
               C9=d9.get("C9"), spatial_class=d9.get("spatial_class"),
               factors=d9.get("factors"), partial=d9.get("partial"),
               t9_detail=d9.get("t9_detail"), s9_detail=d9.get("s9_detail"),
               e9_detail=d9.get("e9_detail"), d7b=d9.get("d7b"),
               C=out.get("C"), horizon=dict(
                   T=out["horizon"]["T_used"],
                   why=out["horizon"]["why_stopped"],
                   traj=out["horizon"]["interest_trajectory"]),
               flags=out.get("flags"), status=out.get("status", "ok"),
               wall=round(time.time() - t0, 1))
    p = os.path.join(outdir, f"{a.name}_s{a.seed}.json")
    with open(p, "w") as f:
        json.dump(AV2.js(row), f, indent=1)
    print(json.dumps(AV2.js(dict(name=a.name, C9=row["C9"],
                                 cls=row["spatial_class"],
                                 f=row["factors"], iv2=row["interest_v2"],
                                 iv3=row["interest_v3"],
                                 wall=row["wall"]))))


if __name__ == "__main__":
    main()
