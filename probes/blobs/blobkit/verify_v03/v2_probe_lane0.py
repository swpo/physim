"""verify_v03/v2_probe_lane0.py — the 7/8 disagreement, isolated.
p2g3_032 seed 1 f32: (a) run_assay_b single (gpu backend), (b) run_assay_batch
with ONE lane (packs alone -> same struct/shape as the single), (c) batch of
2 with a size-7-channel co-passenger (forces nc_max=7 padding like V2's mix).
If (a)==(b) bitwise but (c) differs -> the flip is padded-shape f32 rounding
(XLA kernel/association change), not a ladder bug. Writes V2_probe.json."""
import json, os, sys, time
os.environ.setdefault("BLOBKIT_RESULTS", "")
import blobkit.assay_v2 as A
import blobkit.assay_v2b as AB
from blobkit.soup.backend import get_backend
from blobkit.assay_batch import run_assay_batch

HERE = os.path.dirname(os.path.abspath(__file__))
U4 = ("/Users/spoho/Documents/prime/test/physim/probes/blobs/l0/"
      "deepsearch/final_cpu_harvest/union4_final_cpu.json")
STRIP = {"wall_total", "wall_s", "wall_sim"}

def strip_wall(o):
    if isinstance(o, dict):
        return {k: strip_wall(v) for k, v in o.items() if k not in STRIP}
    if isinstance(o, (list, tuple)):
        return [strip_wall(v) for v in o]
    return o

def canon(out):
    return json.dumps(strip_wall(A.js(out)), sort_keys=True)

def hz(o):
    return dict(interest=o["interest"], T=o["horizon"]["T_used"],
                why=o["horizon"]["why_stopped"],
                decisions=[d["fired"] for d in o["horizon"]["decisions"]])

def main():
    u4 = json.load(open(U4))
    by_cand = {c["cand"]: c for c in u4.values()}
    g0 = dict(by_cand["p2g3_032"]["genome"]); g0["id"] = "p2g3_032"
    gm = dict(by_cand["p5g6_009"]["genome"]); gm["id"] = "p5g6_009"  # nc=4+3ch? forces padding

    t0 = time.time()
    single = AB.run_assay_b(dict(g0), seed=1, results_path=None, verbose=True,
                            backend=get_backend("gpu"), workers=0)
    b1 = run_assay_batch([(dict(g0), 1)], dtype="f32", verbose=True,
                         B_pad=(1,))
    b2 = run_assay_batch([(dict(g0), 1), (dict(gm), 1)], dtype="f32",
                         verbose=True, B_pad=(2,))
    res = dict(gate="V2-probe", world="p2g3_032", seed=1, dtype="f32",
               single=hz(single), batch1=hz(b1[0]), batch2=hz(b2[0]),
               b1_bitwise=(canon(single) == canon(b1[0])),
               b2_bitwise=(canon(single) == canon(b2[0])),
               wall=round(time.time() - t0, 1),
               note=("batch1 packs alone (struct == single); batch2 pads "
                     "channels to the co-passenger's width. b1_bitwise=true "
                     "+ b2_bitwise=false => padded-shape f32 rounding flip "
                     "(seed-level equivalence), not a ladder bug."))
    json.dump(res, open(os.path.join(HERE, "V2_probe.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
