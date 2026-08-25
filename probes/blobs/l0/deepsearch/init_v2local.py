"""init_v2local.py — slim v2-epoch gen-0 (gen=10): 24 representative seeds
re-evaluated under assay_v2 (fresh archive; v1-epoch scores not comparable)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ds2_lib as D2, ds2_gen as G2, ds2_ops as OPS2, genome as G

HERE = os.path.dirname(os.path.abspath(__file__))
old = json.load(open(os.path.join(HERE, "archive_v2_v1epoch.json")))
by_cand = {c["cand"]: c for c in old.values()}
# displaced cands: recover genomes from results rows (v2 then v1)
for path, kind in (("results_v2.json", "ds2_eval"), ("results.json", "ds_eval")):
    try:
        rws = json.load(open(os.path.join(HERE, path)))
    except Exception:
        continue
    for r in rws:
        if (r.get("kind") == kind and r.get("phase") == "screen"
                and r.get("genome") and r["cand"] not in by_cand):
            by_cand[r["cand"]] = dict(cand=r["cand"], genome=r["genome"])
GTS = G2.gt_genomes()
PICK = ["ds3_017", "ds3_014", "ds6_000",
        "ds2g1_017", "ds2g3_015", "ds2g3_005", "ds2g2_016", "ds2g1_010",
        "ds2g1_001", "ds2g2_003", "ds2g2_007", "ds2g2_006",
        "ds5_003", "g0_jit_11", "ds6_012", "ds3_001", "ds4_023"]
jobs = []
for k, g in GTS.items():
    jobs.append(dict(cand=f"v2g10_gt_{k}", gen=10, op="gt", kind="screen",
                     origin="gt", genome=G.genome_json(g)))
for cand in PICK:
    c = by_cand.get(cand)
    if c is None:
        print("MISSING", cand); continue
    g = OPS2.ensure_vtags(dict(c["genome"]), origin=cand)
    jobs.append(dict(cand=f"v2g10_{cand}", gen=10, op="seed", kind="screen",
                     parents=[cand], genome=G.genome_json(g)))
print(len(jobs), "gen-10 jobs")
G2.write_shards(jobs, "g10")
