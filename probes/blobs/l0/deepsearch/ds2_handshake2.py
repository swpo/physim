import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ds2_lib as D2, ds2_gen as G2, genome as G

cfgp = D2.CONFIG
cfg = json.load(open(cfgp)); cfg0 = dict(cfg)
cfg["metrics"] = "v2"
D2.save_config(cfg)
try:
    gts = G2.gt_genomes()
    job = dict(cand="hs2_mv3", gen=-2, op="handshake", kind="hs",
               parents=["gt_mv3"], genome=G.genome_json(gts["mv3"]))
    row = D2.evaluate_v2(job)
    print("hs2_mv3", row.get("status"), "I2=", row.get("interest"),
          "cell=", row.get("cell"), "T=", row.get("T_used"),
          "wall=", row.get("wall_assay"), "npz=", row.get("npz"),
          "hor=", row.get("horizon"), flush=True)
finally:
    D2.save_config(cfg0)
print("HS2_DONE")
