import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import ds2_lib as D2
import ds2_ops as OPS2
import genome as G
import operators_lib as OP

rng = np.random.default_rng(99)
m0 = G.ref_M0()
iso = OP.ref_iso(0.75)

j1g, i1 = OPS2.mint_bilin(m0, rng, "smoke_v0")
j2g, i2 = OPS2.add_chan(iso, rng)
j3g, i3 = OPS2.dup_act(m0, rng, mode="split")
jobs = [
    dict(cand="smk2_mint", gen=-1, op="mint_bilin", kind="smoke", T=800.0,
         params=i1, genome=G.genome_json(j1g)),
    dict(cand="smk2_addch", gen=-1, op="add_chan", kind="smoke", T=800.0,
         params=i2, genome=G.genome_json(j2g)),
    dict(cand="smk2_dup", gen=-1, op="dup_act", kind="smoke", T=800.0,
         params=i3, genome=G.genome_json(j3g)),
]
for j in jobs:
    row = D2.evaluate_v2(j)
    print(j["cand"], row.get("status"), row.get("interest"), row.get("cell"),
          "minted:", row.get("minted"), flush=True)
print("SMOKE_DONE")
