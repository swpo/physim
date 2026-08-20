"""Validate funnel against known physics:
 1) M0 genome: G0 pass; vacuum designated at -0.70354; margin<0.
 2) M4 (A=4): G0c shell wavelength ~10.9 (cert 1%).
 3) M2 (A=5, tau=2.5 Dv=2): oscillatory tails w/ d*~15.7-ish spacing.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
import numpy as np
import genome as G
import funnel as FU

recs = []
for name, gf in [("M0", G.ref_M0), ("M4", lambda: G.ref_M4(5.7)), ("VVW", G.ref_VVW),
                 ("XV", G.ref_XV), ("BFIELD", G.ref_BFIELD)]:
    g = gf()
    u0_ref = [a["u0"] for a in g["acts"]]
    rec = FU.funnel(g)
    u0_des = [a["u0"] for a in g["acts"]]
    out = dict(kind="funnel_check", genome=name, stage=rec["stage"],
               margin=rec.get("g0a_margin"), u0_ref=u0_ref, u0_designated=u0_des,
               vacuum_match=bool(np.allclose(u0_ref, u0_des, atol=1e-4)),
               tails=rec.get("g0c"), chem=rec.get("chem_box"))
    recs.append(out)
    print(json.dumps(out))
    G.append_result(out)

# M2 world: tau=2.5, Dv=2.0 (A=5)
g = G.ref_M0(); g["chans"][0]["tau"]=2.5; g["chans"][0]["D"]=2.0; g["id"]="ref_M2_P7s"
rec = FU.funnel(g)
out = dict(kind="funnel_check", genome="M2_P7s", stage=rec["stage"],
           margin=rec.get("g0a_margin"), tails=rec.get("g0c"))
print(json.dumps(out))
G.append_result(out)
