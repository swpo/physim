import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ds2_lib as D2
import ds2_gen as G2

# temp config flip INSIDE this process only: write cfg, run, restore
cfgp = D2.CONFIG
cfg = json.load(open(cfgp)); cfg0 = dict(cfg)
cfg["metrics"] = "v2"
D2.save_config(cfg)
try:
    a2 = json.load(open(D2.ARCHIVE2))
    picks = {}
    for k, c in a2.items():
        if c["cand"] == "ds2g1_017": picks["hs2_top"] = c
        if c["cand"] == "ds2g3_005": picks["hs2_mint"] = c
        if c["cand"] == "g0_gt_m0": picks["hs2_static"] = c
    print("picks:", {k: v["cand"] for k, v in picks.items()}, flush=True)
    for name, c in picks.items():
        job = dict(cand=name, gen=-2, op="handshake", kind="hs",
                   parents=[c["cand"]], genome=c["genome"], save_npz=False)
        row = D2.evaluate_v2(job)
        print(name, row.get("status"), "I2=", row.get("interest"),
              "cell=", row.get("cell"), "T=", row.get("T_used"),
              "hor=", row.get("horizon"), flush=True)
finally:
    D2.save_config(cfg0)
print("HS_DONE")
