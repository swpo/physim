"""pod_smoke.py — 3-candidate smoke: seed eval (static GT), a mint child,
an extending elite. Validates: imports, funnel, assay_v2 lock, archive insert,
t0 floor, vtags. Exit 0 iff all three rows land with status ok.
Usage: python3 pod_smoke.py"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pod_lib as PL
sys.path.insert(0, os.path.join(HERE, "lib"))
import genome as G
import ds2_ops as OPS2

cfg = PL.config()
P = PL.paths(cfg)
rng = np.random.default_rng(1234)

m0 = G.ref_M0()
m0["id"] = "smoke_m0"
mint, info = OPS2.mint_bilin(G.ref_BFIELD(), rng, "smoke_vertex")
mint["id"] = "smoke_mint"
seeds = {os.path.basename(p): p
         for p in __import__("glob").glob(os.path.join(HERE, "seeds", "*.json"))}
elite_p = seeds.get("ds3_014.json") or sorted(seeds.values())[0]
elite = json.load(open(elite_p))
elite["id"] = "smoke_elite"

jobs = [
    dict(cand="smoke_m0", gen=-1, op="seed", kind="smoke",
         genome=G.genome_json(m0)),
    dict(cand="smoke_mint", gen=-1, op="mint_bilin", kind="smoke",
         params=info, genome=G.genome_json(OPS2.ensure_vtags(mint))),
    dict(cand="smoke_elite", gen=-1, op="seed", kind="smoke", cap=5000.0,
         genome=G.genome_json(OPS2.ensure_vtags(elite, origin="elite"))),
]
ok = True
for j in jobs:
    row = PL.evaluate(j, cfg)
    good = row.get("status") == "ok" and row.get("cell")
    ok &= bool(good)
    print(f'{j["cand"]:14s} status={row.get("status")} I={row.get("interest")} '
          f'T={row.get("T_used")} cell={row.get("cell")} '
          f'minted={row.get("minted")}', flush=True)
    ev, cell = PL.archive_insert(row, P)
    print(f'  archive: {ev} {cell}', flush=True)
print("SMOKE", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
